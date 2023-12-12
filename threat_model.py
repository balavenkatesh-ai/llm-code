import json
import os

import streamlit as st
import streamlit.components.v1 as components
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from huggingface_hub import hf_hub_download

# Define the GPT prompt templates
threat_model_template = """
    <s>[INST] <<SYS>> Act as a cyber security expert with more than 20 years experience of using the STRIDE threat modelling methodology to produce comprehensive threat models for a wide range of applications. Your task is to use the application description provided to you to produce a list of specific threats for the application. Your analysis should provide a credible scenario in which each threat could occur in the context of the application. It is very important that your responses are tailored to reflect the details you are given.

    In addition to the description, you will be provided with the following key details about the application that you will need to consider when producing your threat model:
    - The type of application
    - The methods used to authenticate users to the application
    - Whether or not the application is internet-facing
    - Whether or not the application processes sensitive data
    - Whether or not the application uses privileged access management to protect privileged accounts
    
    <</SYS>>

    Below is the application description and key details:
    APPLICATION TYPE: {app_type}
    AUTHENTICATION METHODS: {authentication}
    INTERNET FACING: {internet_facing}
    SENSITIVE DATA: {sensitive_data}
    PRIVILEGED ACCESS MANAGEMENT: {pam}
    APPLICATION DESCRIPTION: {app_input}

    Your output should be in the form of a markdown table with the following columns:
    - Column A: Threat Type
    - Column B: Scenario
    - Column C: Potential Impact
    
    In addition to the table you should also make some suggestions to the user on how they can improve the application description to enable you to produce a more comprehensive threat model.

    YOUR RESPONSE:
    {{
        "threat_table": "YOUR THREAT TABLE HERE",
        "improvement_suggestions": "YOUR IMPROVEMENT SUGGESTIONS HERE"
    }} [/INST]
"""

attack_tree_template = """
    <s>[INST] <<SYS>> Act as a cyber security expert with more than 20 years experience of creating attack trees to communicate the likely routes by which systems and applications will be attacked by adversaries. Your task is to use the application description provided to you to generate an attack tree for the application. Your analysis should be based on credible attack types that could occur given the context of the application. It is very important that your responses are tailored to reflect the details you are given.

    In addition to the description, you will be provided with the following key details about the application that you will need to consider when producing the attack tree:
    - The type of application
    - The methods used to authenticate users to the application
    - Whether or not the application is internet-facing
    - Whether or not the application processes sensitive data
    - Whether or not the application uses privileged access management to protect privileged accounts
    
    <</SYS>>

    Below is the application description and key details:
    APPLICATION TYPE: {app_type}
    AUTHENTICATION METHODS: {authentication}
    INTERNET FACING: {internet_facing}
    SENSITIVE DATA: {sensitive_data}
    PRIVILEGED ACCESS MANAGEMENT: {pam}
    APPLICATION DESCRIPTION: {app_input}
    
    Your output should be in the form of a JSON object that contains two key-value pairs. The first key is 'mermaid_code' which should contain a string of valid Mermaid code that represents an attack tree. Mermaid is a simple markdown-like script language for generating charts from text via JavaScript.

    IMPORTANT: When generating Mermaid code, you MUST ALWAYS enclose the node and link labels in double quotation marks to escape any special characters. For example:
    ```
    graph TD
    A["Attacker"] -->|"Phishing attack"| B["User's credentials"]
    A -->|"Cross-site scripting (XSS)"| F["User's session"]
    A -->|"Cross-site request forgery (CSRF)"| G["User's session"]
    A -->|"Server-side request forgery (SSRF)"| H["Server resources"]
    ```
    
    The second key-value pair is 'improvement_suggestions' and it should contain some suggestions to the user on how they can improve the application description to enable you to produce a more comprehensive and accurate attack tree.

    YOUR RESPONSE:
    {{
        "mermaid_code": `YOUR MERMAID CODE HERE`,
        "improvement_suggestions": "YOUR IMPROVEMENT SUGGESTIONS HERE"
    }} [/INST]
"""

mitigations_template = """
    <s>[INST] <<SYS>> Act as a cyber security expert with more than 20 years experience of using the STRIDE threat modelling methodology. Your task is to provide potential mitigations for the threats identified in the threat model. 
    It is very important that your responses are tailored to reflect the details of the threats. <</SYS>>

    Your output should be in the form of a markdown table with the following columns:
    - Column A: Threat Type
    - Column B: Scenario
    - Column C: Suggested Mitigation(s)

    Below is the list of identified threats:
    {threats}

    YOUR RESPONSE: [/INST]
"""

# Create a PromptTemplate objects with the specified input variables
threat_model_prompt = PromptTemplate(
    input_variables=["app_type", "authentication", "internet_facing", "sensitive_data", "pam", "app_input"],
    template=threat_model_template,
)

attack_tree_prompt = PromptTemplate(
    input_variables=["app_type", "authentication", "internet_facing", "sensitive_data", "pam", "app_input"],
    template=attack_tree_template,
)

mitigations_prompt = PromptTemplate(
    input_variables=["threats"],
    template=mitigations_template,
)

# Function to load LLM (Language Model) with given API key and model name
def load_LLM():
    model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
    model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin"
    if os.path.exists(model_basename):
        st.write("Using locally available model...")
        model_path = model_basename
    else:
        st.write("Downloading model...")
        model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)
        
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    n_gpu_layers = 40
    n_batch = 512

    llm = LlamaCpp(
        model_path=model_path,
        max_tokens=2024,
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        callback_manager=callback_manager,
        verbose=True,
        n_ctx=4096,
        stop=['USER:'],
        temperature=0.2,
    )
    
    return llm


st.title("MSBR - Threat LLM Model")

# Function to get user input for the application description and key details
def get_input():
    input_text = st.text_area(label="Describe the application to be modelled", placeholder="Enter your application details...", height=150, key="app_input", help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.")
    return input_text

# Function to render Mermaid diagram
def mermaid(code: str, height: int = 500) -> None:
    components.html(
        f"""
        <pre class="mermaid" style="height: {height}px;">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height=height,
    )

# Function to extract Mermaid code from LLM output
def extract_mermaid_code(llm_output: dict) -> str:
    return llm_output.get("mermaid_code", "") # Return empty string if key does not exist

# Get application description from the user
app_input = get_input()

# Create two columns layout for input fields
col1, col2 = st.columns(2)

# Create input fields for app_type, sensitive_data and pam
with col1:
    app_type = st.selectbox(
        label="Select the application type", 
        options=["Web application", "Mobile application", "Desktop application", "Cloud application", "IoT application", "Other"], 
        key="app_type"
        )

    sensitive_data = st.selectbox(
        label="What is the highest sensitivity level of the data processed by the application?",
        options=["Top Secret", "Secret", "Confidential", "Restricted", "Unclassified", "None"],
        key="sensitive_data"
        )
    
    pam = st.selectbox(
        label="Are privileged accounts stored in a Privileged Access Management (PAM) solution?",
        options=["Yes", "No"],
        key="pam"
    )

# Create input fields for internet_facing and authentication
with col2:
    internet_facing = st.selectbox(
        label="Is the application internet-facing?", 
        options=["Yes", "No"], 
        key="internet_facing"
        )
    
    authentication = st.multiselect(
        'What authentication methods are supported by the application?',
        ['SSO', 'MFA', 'OAUTH2', 'Basic', 'None'],
        key="authentication"
    )


# Function to safely parse JSON output from the LLM
def parse_llm_output(output: str) -> dict:
    try:
        return json.loads(output)
    except json.JSONDecodeError: # Handle JSONDecodeError if the output cannot be parsed as JSON
        st.error("The language model output could not be parsed as JSON.")
        return {}

# Create a collapsible section for Threat Modelling
with st.expander("Threat Model", expanded=False):
    # Create a submit button for Threat Modelling
    threat_model_submit_button = st.button(label="Generate Threat Model")

    # If the Generate Threat Model button is clicked and the user has provided an application description
    if threat_model_submit_button and app_input:
        # Load the Language Model with the provided API key
        llm = load_LLM()
        
        llm_chain = LLMChain(prompt=threat_model_prompt, llm=llm)
            
        chain_input = {
        'app_type':app_type, 'authentication':authentication, 'internet_facing':internet_facing, 
        'sensitive_data':sensitive_data, 'pam':pam, 'app_input':app_input
        }
        
        with st.spinner("Analysing potential threats..."):
            raw_model_output = llm_chain.run(chain_input)
            
        st.write(raw_model_output)

        # # Format the prompt with the user-provided details
        # prompt_with_details = threat_model_prompt.format(app_type=app_type, authentication=authentication, internet_facing=internet_facing, sensitive_data=sensitive_data, pam=pam, app_input=app_input)
            
        # # Show a spinner while generating the threat model
        # with st.spinner("Analysing potential threats..."):
        #     raw_model_output = llm(prompt_with_details)

        # # Parse the LLM output into a Python dictionary
        # model_output_dict = parse_llm_output(raw_model_output)

        # # Extract the markdown table and improvement suggestions
        # threat_table = model_output_dict.get("threat_table", "No threats identified.")
        # improvement_suggestions = model_output_dict.get("improvement_suggestions", "No suggestions provided.")

        # # Store threat_table in session state
        # st.session_state["threat_table"] = threat_table

        # # Display the generated threat model and improvement suggestions
        # st.write("Threat Table:")
        # st.write(threat_table)
        # st.write("Improvement Suggestions:")
        # st.write(improvement_suggestions)

        # Add a button to allow the user to download the output as a Markdown file
        st.download_button(
        label="Download Output",
        data=raw_model_output,
        file_name="stride_gpt_threat_model.md",
        mime="text/markdown",
        )

    # If the submit button is clicked and the user has not provided an application description
    if threat_model_submit_button and not app_input:
        st.error("Please enter your application details before submitting.")

# Create a collapsible section for Attack Tree
with st.expander("Attack Tree", expanded=False):

    # Create a submit button for Attack Tree
    attack_tree_submit_button = st.button(label="Generate Attack Tree")

    # If the Generate Attack Tree button is clicked and the user has provided an application description
    if attack_tree_submit_button and app_input:
        # Load the Language Model with the provided API key
        llm = load_LLM()
        
        llm_chain = LLMChain(prompt=threat_model_prompt, llm=llm)
            
        chain_input = {
        'app_type':app_type, 'authentication':authentication, 'internet_facing':internet_facing, 
        'sensitive_data':sensitive_data, 'pam':pam, 'app_input':app_input
        }
        
        with st.spinner("Generating attack tree..."):
            raw_model_output = llm_chain.run(chain_input)
            
        st.write(raw_model_output)

        # # Format the prompt with the user-provided details
        # prompt_with_details = attack_tree_prompt.format(app_type=app_type, authentication=authentication, internet_facing=internet_facing, sensitive_data=sensitive_data, pam=pam, app_input=app_input)

        # # Show a spinner while generating the attack tree
        # with st.spinner("Generating attack tree..."):
        #     raw_model_output = llm(prompt_with_details)

        #     # Parse the LLM output into a Python dictionary
        #     model_output_dict = parse_llm_output(raw_model_output)

        #     # Extract the Mermaid code and improvement suggestions
        #     mermaid_code = model_output_dict.get("mermaid_code", "No Mermaid code provided.")
        #     improvement_suggestions = model_output_dict.get("improvement_suggestions", "No suggestions provided.")

        #     # Display the generated attack tree and improvement suggestions
        #     st.write("Attack Tree:")
        #     st.code(mermaid_code)
        #     st.write("Improvement Suggestions:")
        #     st.write(improvement_suggestions)

            # Add a button to allow the user to download the output as a Markdown file
        st.download_button(
        label="Download Attack Tree",
        data=raw_model_output,
        file_name="stride_gpt_attack_tree.md",
        mime="text/markdown",
        )

        st.markdown("""
        ### Attack Tree Visualisation
        """)

        # Inform the user that the Mermaid visualisation feature is experimental
        st.info("Please note that this feature is experimental. To view the attack tree in detail and/or edit the diagram visit [Mermaid Live](https://mermaid.live) and paste the generated Mermaid code into the editor.")

        # Visualise the attack tree using the Mermaid custom component
        #mermaid(mermaid_code)

    # If the submit button is clicked and the user has not provided an application description
    if threat_model_submit_button and not app_input:
        st.error("Please enter your application details before submitting.")


# Create a collapsible section for Mitigations
with st.expander("Mitigations", expanded=False):
    # Create a submit button for Mitigations
    mitigations_submit_button = st.button(label="Suggest Mitigations")

    # If the Suggest Mitigations button is clicked and the user has provided an application description
    if mitigations_submit_button and app_input:
        # Load the Language Model with the provided API key
        llm = load_LLM()

        # Format the mitigations prompt with the threats from the threat model
        prompt_with_threats = mitigations_prompt.format(threats=st.session_state["threat_table"])

        # Show a spinner while suggesting mitigations
        with st.spinner("Suggesting mitigations..."):
            model_output = llm(prompt_with_threats)

        # Display the suggested mitigations
        st.write(model_output)

        # Add a button to allow the user to download the output as a Markdown file
        st.download_button(
        label="Download Mitigations",
        data=model_output,
        file_name="stride_gpt_mitigations.md",
        mime="text/markdown",
        )

    # If the submit button is clicked and the user has not provided an application description
    if mitigations_submit_button and not app_input:
        st.error("Please enter your application details before submitting.")
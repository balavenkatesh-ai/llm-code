import streamlit as st
import time
import os
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from huggingface_hub import hf_hub_download


st.title("MSBR - Threat LLM Model")

model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin"

# model_name_or_path = "AIDC-ai-business/Marcoroni-70B-v1"
# model_basename = "pytorch_model-00015-of-00015.bin"


# st.write("Downloading model...")
# model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)

if os.path.exists(model_basename):
    st.write("Using locally available model...")
    model_path = model_basename
else:
    st.write("Downloading model...")
    model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)


# Define your Streamlit input
component_name = st.text_input("Enter your Threat Component Name:")
component_version = st.text_input("Enter your Threat Component Version:")


if st.button("Generate MSBR Threat Report"):
    st.write("Generating response...")
    with st.spinner("Processing..."):
    
        response_placeholder = st.empty()
        
        # template = """''SYSTEM: You are an expert in cyber security.
        # USER: Give me list of 20 three details such as threat name, attack domain and threat description for {question} component in CSV format
        #     For Example:
        # Threat Name,Attack Domain,Threat Description,Countermeasure
        # SQL Injection,Web Application,An attacker can inject malicious SQL code into a web application's database queries to gain unauthorized access or manipulate data.
        
        # ASSISTANT: """

        # Rest of your code
        template = """Act as a cyber security expert.Create a list of 20 threat names, Attack domains, threat description,and countermeasure for the 
        given {component_name} component and version of component is {component_version}. The output format should be in dictionary format. 
        
        Each threat name should be unique and descriptive of the potential attack. 
        The attack domain should describe the type of attack(e.g., network,application,etc.). 
        The threat description should provide a brief explanation of the potential attack.
        Countermeasure for corresponding threats.
        
        Sample Output:
        "Threat Name" : Data Manipulation,	"Attack Domain" : Application,"Threat Description" : "Attackers can modify data in MongoDB if there's a lack of proper access controls or vulnerabilities in the application using the database.",	
        "Countermeasure" : "Architecture and Design Implementation REALIZATION: This weakness is caused during implementation of an architectural security tactic.
        If a programmer believes that an attacker cannot modify certain inputs, then the programmer might not perform any input validation at all. For example, in web applications, many programmers believe that cookies and hidden form fields can not be modified from a web browser (CWE-472), although they can be altered using a proxy or a custom program. In a client-server architecture, the programmer might assume that client-side security checks cannot be bypassed, even when a custom client could be written that skips those checks (CWE-602)."
        
        """
                    
        prompt = PromptTemplate(template=template, input_variables=["component_name","component_version"])

        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        n_gpu_layers = 40
        n_batch = 512

        llm = LlamaCpp(
            model_path=model_path,
            max_tokens=1024,
            n_gpu_layers=n_gpu_layers,
            n_batch=n_batch,
            callback_manager=callback_manager,
            verbose=True,
            n_ctx=4096,
            #stop=['USER:'],
            temperature=0.1,
        )

        llm_chain = LLMChain(prompt=prompt, llm=llm)
        
        chain_input = {
        'component_name': component_name,
        'component_version': component_version
        }

        response = llm_chain.run(chain_input)
        st.write("Generated MSBR LLM Threat Report:")
        # Split the response into rows and columns
        csv_rows = [row.split(',') for row in response.strip().split('\n')]
        
        # Remove rows with "<NA>"
        csv_rows = [row for row in csv_rows if not all(cell.strip() == "<NA>" for cell in row)]

        st.table(csv_rows)
    #st.write(response)
    
    
    
llm_question = st.text_input("Ask question to LLM model:")

if st.button("Call LLM model"):
    st.write("Generating response...")
    with st.spinner("Processing..."):
    
        response_placeholder = st.empty()
        
        # template = """''SYSTEM: You are an expert in cyber security.
        # USER: Give me list of 20 three details such as threat name, attack domain and threat description for {question} component in CSV format
        # ASSISTANT: """

        # Rest of your code
        template = """Act as a cyber security expert.
        Your task is to answer the following question based on this area of knowledge {llm_question}
        """
                    
        prompt = PromptTemplate(template=template, input_variables=["llm_question"])

        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        n_gpu_layers = 40
        n_batch = 512

        llm = LlamaCpp(
            model_path=model_path,
            max_tokens=1024,
            n_gpu_layers=n_gpu_layers,
            n_batch=n_batch,
            callback_manager=callback_manager,
            verbose=True,
            n_ctx=4096,
            #stop=['USER:'],
            temperature=0.1,
        )

        llm_chain = LLMChain(prompt=prompt, llm=llm)
        

        response = llm_chain.run(llm_question)
        st.write("Response:")
        st.write(response)
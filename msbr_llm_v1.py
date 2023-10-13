import streamlit as st
import time
import os
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from huggingface_hub import hf_hub_download
import pandas as pd

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


if st.button("Generate Threat"):
    if component_name and component_version:
        st.write("Generating response...")
        with st.spinner("Processing..."):
        
            response_placeholder = st.empty()
            
            # template = """''SYSTEM: You are an expert in cyber security.
            # USER: Give me list of 20 three details such as threat name, attack domain and threat description for {question} component in CSV format
            #     For Example:
            # Threat Name,Attack Domain,Threat Description,Countermeasure
            # SQL Injection,Web Application,An attacker can inject malicious SQL code into a web application's database queries to gain unauthorized access or manipulate data.
            #Note:-Additionally, please provide a reference source or details to verify the accuracy of the threat information provided.
            # ASSISTANT: """

            # Rest of your code
            template = """SYSTEM: As a cyber security expert, your task is to prepare list of 20 threats in table Format.
            USER: Please provide Threat Names, Attack Domains, Threat Descriptions,Countermeasures and Reference  for the {component_name} component, version {component_version}.
                
            To structure your data, follow these guidelines:

            1. Threat Name: A descriptive name for each potential threat (e.g., Data Manipulation).
            2. Attack Domain: Specify the category of attack, such as network or application.
            3. Threat Description: Offer a concise explanation of the potential attack. For example, describe how attackers can manipulate data in MongoDB due to improper access controls or vulnerabilities in the application using the database.
            4. Countermeasure: Suggest recommendations to mitigate each threat.
            5. Reference:Provide a reference source name or url to verify the accuracy of the threat information provided.
                        
            ASSISTANT: 
            """
                        
            prompt = PromptTemplate(template=template, input_variables=["component_name","component_version"])

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

            llm_chain = LLMChain(prompt=prompt, llm=llm)
            
            chain_input = {
            'component_name': component_name,
            'component_version': component_version
            }

            response = llm_chain.run(chain_input)
            st.write("Generated MSBR LLM Threat Report:")
            # Split the response into rows and columns
            # csv_rows = [row.split(',') for row in response.strip().split('\n')]
            
            # # Remove rows with "<NA>"
            # csv_rows = [row for row in csv_rows if not all(cell.strip() == "<NA>" for cell in row)]
            #df = pd.DataFrame([response])
            st.markdown(response)
        #st.write(response)
    else:
        st.warning("Please provide a valid Threat Component details.") 
        
    
llm_question = st.text_input("Ask question to LLM model:")

if st.button("Call LLM model") :
    if llm_question:
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
                temperature=0.3,
            )

            llm_chain = LLMChain(prompt=prompt, llm=llm)
            

            response = llm_chain.run(llm_question)
            st.write("Response:")
            st.write(response)
    else:
        st.warning("Please provide a input.") 
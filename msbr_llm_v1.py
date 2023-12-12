import streamlit as st
import time
import os
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from huggingface_hub import hf_hub_download
import pandas as pd
import json

st.title("MSBR - Component Threat Library")

model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin"

# model_name_or_path = "TheBloke/Llama-2-70B-GGUF"
# model_basename = "llama-2-70b.Q4_K_M.gguf"

def parse_llm_output(output: str) -> dict:
    try:
        return json.loads(output)
    except json.JSONDecodeError: # Handle JSONDecodeError if the output cannot be parsed as JSON
        st.error("The language model output could not be parsed as JSON.")
        return {}


# st.write("Downloading model...")
# model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)

if os.path.exists(model_basename):
    #st.write("Using locally available model...")
    model_path = model_basename
else:
    st.write("Downloading model...")
    model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)


# Define your Streamlit input
component_name = st.text_input("Enter your Threat Component Name:")
component_version = st.text_input("Enter your Threat Component Version:")
number_of_threat = st.text_input("Enter number of threat wants to generate:")

if st.button("Generate Threat"):
    if component_name and component_version:
        st.write("Generating response...")
        with st.spinner("Processing..."):
        
            response_placeholder = st.empty()
            
            template = """ <s>[INST] <<SYS>>
            As a cyber security expert, your task is to prepare a list of {number_of_threat} threats.It is very important that your responses are tailored to reflect the details you are given.
            <</SYS>>
            
            Provide the following information for each potential threat identified in the {component_name} {component_version} security analysis:
            
            Please follow these guidelines when structuring your data:

            Threat Name: A descriptive name for each potential threat (e.g., Data Manipulation).
            Attack Domain: Specify the category of attack, such as network or application.
            Threat Description: Offer a concise explanation of the potential attack. For example, describe how attackers can manipulate data in {component_name} due to improper access controls or vulnerabilities in the application using the database.
            Countermeasure: Suggest recommendations to mitigate each threat.
            MITRE Tactics ID: Specify the corresponding MITRE Tactics ID from the MITRE ATT&CK® framework (e.g., T1190).
            MITRE Tactics Description: Provide a brief description of the MITRE Tactics ID from the MITRE ATT&CK® framework.
            MITRE Techniques ID: Specify the relevant MITRE Techniques ID from the MITRE ATT&CK® framework (e.g., T1543).
            MITRE Techniques Description: Offer a concise explanation of the MITRE Techniques ID from the MITRE ATT&CK® framework.
            CAPEC Reference URL: Include the URL of the Common Attack Pattern Enumeration and Classification (CAPEC) database entry for each threat, linking to its CAPEC page.
            References: Provide reference source names or URLs to verify the accuracy of the threat information provided.
                        
            Note:- Your output should be in the pandas dataframe table format with the following given above columns. [/INST]
            """
                        
            prompt = PromptTemplate(template=template, input_variables=["component_name","component_version","number_of_threat"])

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
            'component_version': component_version,
            'number_of_threat':number_of_threat
            }

            response = llm_chain.run(chain_input)
            #st.write("Generated MSBR LLM Threat Report:")
            # Split the response into rows and columns
            # csv_rows = [row.split(',') for row in response.strip().split('\n')]
            
            # # Remove rows with "<NA>"
            # csv_rows = [row for row in csv_rows if not all(cell.strip() == "<NA>" for cell in row)]
            #df = pd.DataFrame([response])
            
            st.write(response)
            #st.table(response)
            
            st.download_button(label="Download Output",
                            data=response,
                            file_name="msbr_llm_threat_model.md",
                            mime="text/markdown",)
        #st.write(response)
    else:
        st.warning("Please provide a valid Threat Component details.") 
        


        
    
llm_question = st.text_input("Ask security related question to LLM model:")

if st.button("Call LLM model") :
    if llm_question:
        st.write("Generating response...")
        with st.spinner("Processing..."):
        
            response_placeholder = st.empty()

            template = """ <s>[INST] <<SYS>>
            Act as a cyber security expert.Your task is to answer the following question based on this area of knowledge.
            <</SYS>>
            
            {llm_question} [/INST]
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
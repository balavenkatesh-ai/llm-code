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

st.title("MSBR - LLM Model Scanning")

model_name_or_path = "TheBloke/LlamaGuard-7B-GGUF"
model_basename = "llamaguard-7b.Q5_K_M.gguf"

#model_path = "/root/.cache/huggingface/hub/models--TheBloke--LlamaGuard-7B-GGUF/snapshots/272da9e9931d3b20f0c53cb7fd8e736f61fd4b63/llamaguard-7b.Q5_K_M.gguf"


if os.path.exists(model_basename):
    #st.write("Using locally available model...")
    model_path = model_basename
else:
    st.write("Downloading model...")
    model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)


# Define your Streamlit input
prompt = st.text_input("Enter your input Prompt:")


if st.button("Scan"):
    if prompt:
        st.write("Generating response...")
        with st.spinner("Processing..."):
        
            response_placeholder = st.empty()
            
            # template = """ <s>[INST] <<SYS>>
            # As a cyber security expert, your task is to prepare a list of {number_of_threat} threats.It is very important that your responses are tailored to reflect the details you are given.
            # <</SYS>>
            
            # Provide Threat Names, Attack Domains, Threat Descriptions, Countermeasures, CAPEC Reference URLs, and References for the {component_name} component, version {component_version}.

            # To structure your data, follow these guidelines:

            # 1. Threat Name: A descriptive name for each potential threat (e.g., Data Manipulation).
            # 2. Attack Domain: Specify the category of attack, such as network or application.
            # 3. Threat Description: Offer a concise explanation of the potential attack. For example, describe how attackers can manipulate data in MongoDB due to improper access controls or vulnerabilities in the application using the database.
            # 4. Countermeasure: Suggest recommendations to mitigate each threat.
            # 5. CAPEC Reference URL: Include the URL of the CAPEC (Common Attack Pattern Enumeration and Classification) database for each threat, linking to its CAPEC page.
            # 6. References: Provide reference source names or URLs to verify the accuracy of the threat information provided.
                        
            # Note:- Your output should be in the pandas dataframe table format with the following given above columns. [/INST]
            # """
            
            template =  """<s>[INST]
                        {prompt}
            [/INST]
            """
                        
            prompt = PromptTemplate(template=template, input_variables=["prompt"])

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
            'prompt': prompt
            }

            response = llm_chain.run(chain_input)
            st.write(response)
    else:
        st.warning("Please provide a valid Threat Component details.") 
        
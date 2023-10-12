import streamlit as st
import time
import os
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from huggingface_hub import hf_hub_download

from langchain.output_parsers import PydanticOutputParser

from pydantic import BaseModel

class ThreatResponse(BaseModel):
    threat_name: str
    attack_domain: str
    threat_description: str

pydantic_parser = PydanticOutputParser(pydantic_object=ThreatResponse)


st.title("MSBR - Threat LLM Model")

model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin"

# st.write("Downloading model...")
# model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)

if os.path.exists(model_basename):
    st.write("Using locally available model...")
    model_path = model_basename
else:
    st.write("Downloading model...")
    model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)


# Define your Streamlit input
question = st.text_input("Enter your Threat Component Name:")
if st.button("Submit"):
    st.write("Generating response...")
    
    response_placeholder = st.empty()
    
    # template = """''SYSTEM: You are an expert in cyber security.
    # USER: Give me list of 20 three details such as threat name, attack domain and threat description for {question} component in CSV format
    # ASSISTANT: """

    # Rest of your code
    template = """Act as a cyber security expert.Create a list of 20 threat names, Attack domains,and threat description for the 
    given {question} component in CSV format. Each threat name should be unique and descriptive of the potential attack. The attack domain
    should describe the type of attack(e.g., network,application,etc.). The threat description should provide a brief explanation of the potential attack.
    
    For Example:
    Threat Name,Attack Domain,Threat Description
    SQL Injection,Web Application,An attacker can inject malicious SQL code into a web application's database queries to gain unauthorized access or manipulate data.
    """
                
    prompt = PromptTemplate(template=template, input_variables=["question"])

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

    response = llm_chain.run(question)
    #pytantic response
    parsed_response = pydantic_parser.parse(response)
    
    # st.write("Response:")
    # st.write(response)
    
    st.write("Parsed Response:")
    st.write(parsed_response.dict())


    # Start generating the response
    # with response_placeholder:
    #     response_placeholder.empty()  # Clear the initial "Generating response..." message
    #     for _ in range(5):  # You can adjust the number of iterations as needed
    #         response = llm_chain.run(question)
    #         st.write("Response:")
    #         st.write(response)
    #         time.sleep(2) 
    
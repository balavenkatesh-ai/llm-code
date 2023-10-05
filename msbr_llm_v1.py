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
    template = """You are an expert in cyber security. I am generating threat mapping CSV file.
    write list of 20 three details such as threat name, attack domain and threat description for {question} 
    component in CSV format.
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
    st.write("Response:")
    st.write(response)


    # Start generating the response
    # with response_placeholder:
    #     response_placeholder.empty()  # Clear the initial "Generating response..." message
    #     for _ in range(5):  # You can adjust the number of iterations as needed
    #         response = llm_chain.run(question)
    #         st.write("Response:")
    #         st.write(response)
    #         time.sleep(2) 
    
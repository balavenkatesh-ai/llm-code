import streamlit as st
import os
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from huggingface_hub import hf_hub_download
from utils import convert_to_csv, json_to_csv
import datetime

st.title("MSBR - Component Threat Library")

model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin"

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
            
            response_schemas = [
            ResponseSchema(
                name="Threat Name", description="A descriptive name for each potential threat (e.g., Data Manipulation)"),
            ResponseSchema(
                name="Threat Description",
                description="Offer a concise explanation of the potential attack. For example, describe how attackers can manipulate data in given component name due to improper access controls or vulnerabilities in the application using the database.",
            ),
            ResponseSchema(
                name="Attack Domain", description="Specify the category of attack, such as network or application"),
            ResponseSchema(
                name="Countermeasure",
                description="Suggest recommendations to mitigate each threat",
            ),
            ResponseSchema(
                name="MITRE Tactics ID", description="Specify the corresponding MITRE Tactics ID URL from the MITRE ATT&CK® framework (e.g., https://attack.mitre.org/tactics/TA0043/)"),
            ResponseSchema(
                name="MITRE Tactics Description",
                description="Provide a brief description of the MITRE Tactics ID from the MITRE ATT&CK® framework.",
            ),
            
             ResponseSchema(
                 name="MITRE Techniques ID", description=" Specify the relevant MITRE Techniques ID URL from the MITRE ATT&CK® framework (e.g., https://attack.mitre.org/techniques/T1548/)"),
            ResponseSchema(
                name="MITRE Techniques Description",
                description="Offer a concise explanation of the MITRE Techniques ID from the MITRE ATT&CK® framework",
            ),
            ResponseSchema(
                name="CAPEC Reference URL", description="Include the URL of the Common Attack Pattern Enumeration and Classification (CAPEC) database entry for each threat, linking to its CAPEC page(e.g.,https://capec.mitre.org/data/definitions/1000.html)"),
            # ResponseSchema(
            #     name="NIST Reference",
            #     description="Provide relevant information or recommendations from the National Institute of Standards and Technology (NIST)",
            # ),
            # ResponseSchema(name="CSA-CCM Reference", description="Include details or guidelines from the Cloud Security Alliance Cloud Controls Matrix (CSA-CCM)"),
            # ResponseSchema(
            #     name="ISO27K Reference",
            #     description="Incorporate information or standards from the ISO/IEC 27000 series.",
            # ),
            # ResponseSchema(name="OWASP Reference", description="Integrate insights or recommendations from the Open Web Application Security Project (OWASP)"),
            # ResponseSchema(
            #     name="SANS Referenc",
            #     description=" Include relevant details or best practices from the SysAdmin, Audit, Network, Security (SANS) Institute",
            # ),
            ]
            
            
            template = """ <s>[INST] <<SYS>>
            Act as a cyber security expert with more than 30 years experience of threat library development for given {component_name} {component_version}, your task is to prepare a list of {number_of_threat} threats.It is very important that your responses are tailored to reflect the details you are given.
            
            <</SYS>>
            {format_instructions}
            [/INST]
            """
            
            #output_parser = CommaSeparatedListOutputParser()
            output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
            
            format_instructions = output_parser.get_format_instructions()
                        
            prompt = PromptTemplate(template=template, 
                                    input_variables=["component_name","component_version","number_of_threat"],
                                    partial_variables={"format_instructions": format_instructions},
                                    )

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
                temperature=0,
            )

            llm_chain = LLMChain(prompt=prompt, llm=llm)
            
            chain_input = {
            'component_name': component_name,
            'component_version': component_version,
            'number_of_threat':number_of_threat
            }

            response = llm_chain.run(chain_input)
        
            #response = output_parser.parse(response)
            st.write(response)
            #st.table(response)
        
            # file_name_path = 'llm_results/' + str(component_name) + "-" + str(component_version) + "-"+ str(datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")) +".txt"
            
            # with open(file_name_path,'w') as output:
            #     output.write(response)
                
            file_name = str(component_name) + "-" + str(component_version) + "-"+ str(datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")) +".csv"
            #csv_data = convert_to_csv(response,file_name_path)
            csv_data = json_to_csv(response)
            
            st.download_button(label="Export",
                            data=csv_data,
                            file_name=file_name,
                            mime="text/csv",
                        )
        #st.write(response)
    else:
        st.warning("Please provide a valid Threat Component details.") 
        


        
    
# llm_question = st.text_input("Ask security related question to LLM model:")

# if st.button("Call LLM model") :
#     if llm_question:
#         st.write("Generating response...")
#         with st.spinner("Processing..."):
        
#             response_placeholder = st.empty()

#             template = """ <s>[INST] <<SYS>>
#             Act as a cyber security expert.Your task is to answer the following question based on this area of knowledge.
#             <</SYS>>
            
#             {llm_question} [/INST]
#             """
                        
#             prompt = PromptTemplate(template=template, input_variables=["llm_question"])

#             callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

#             n_gpu_layers = 40
#             n_batch = 512

#             llm = LlamaCpp(
#                 model_path=model_path,
#                 max_tokens=1024,
#                 n_gpu_layers=n_gpu_layers,
#                 n_batch=n_batch,
#                 callback_manager=callback_manager,
#                 verbose=True,
#                 n_ctx=4096,
#                 #stop=['USER:'],
#                 temperature=0.3,
#             )

#             llm_chain = LLMChain(prompt=prompt, llm=llm)
            

#             response = llm_chain.run(llm_question)
#             st.write("Response:")
#             st.write(response)
#     else:
#         st.warning("Please provide a input.") 

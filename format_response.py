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
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

st.title("MSBR - Component Threat Library")

model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin"

if os.path.exists(model_basename):
    #st.write("Using locally available model...")
    model_path = model_basename
else:
    #st.write("Downloading model...")
    model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)


hide_bar= """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        visibility:hidden;
        width: 0px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        visibility:hidden;
    }
    </style>
"""

# --- USER AUTHENTICATION ---
names = ["bala", "arun","kannan"]
usernames = ["bala", "arun","kannan"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "main_dashboard", "abcdef")

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")
    st.markdown(hide_bar, unsafe_allow_html=True)

if authentication_status == None:
    st.warning("Please enter your username and password")
    st.markdown(hide_bar, unsafe_allow_html=True)


if authentication_status:
    
    st.sidebar.title(f"Welcome {name}")
    authenticator.logout("Logout", "sidebar")
    # Define your Streamlit input
    component_name = st.text_input("Enter your Threat Component Name:")
    component_version = st.text_input("Enter your Threat Component Version:")
    number_of_threat = st.text_input("Enter number of threat wants to generate:")

    if st.button("Generate Threat"):
        if component_name and component_version:
            st.write("Generating response...")
            with st.spinner("Processing..."):
            
                response_placeholder = st.empty()
                
                # response_schemas = [
                # ResponseSchema(
                #     name="Threat Name", description="A descriptive name for each potential threat (e.g., Data Manipulation)"),
                # ResponseSchema(
                #     name="Threat Description",
                #     description="Offer a concise explanation of the potential attack. For example, describe how attackers can manipulate data in given component name due to improper access controls or vulnerabilities in the application using the database.",
                # ),
                # ResponseSchema(
                #     name="Attack Domain", description="Specify the category of attack, such as network or application"),
                # ResponseSchema(
                #     name="Countermeasure",
                #     description="Suggest recommendations to mitigate each threat",
                # ),
                # ResponseSchema(
                #     name="MITRE Tactics ID", description="Specify the corresponding MITRE Tactics ID URL from the MITRE ATT&CK® framework (e.g., https://attack.mitre.org/tactics/TA0043/)"),
                # ResponseSchema(
                #     name="MITRE Tactics Description",
                #     description="Provide a brief description of the MITRE Tactics ID from the MITRE ATT&CK® framework.",
                # ),
                
                #  ResponseSchema(
                #      name="MITRE Techniques ID", description=" Specify the relevant MITRE Techniques ID URL from the MITRE ATT&CK® framework (e.g., https://attack.mitre.org/techniques/T1548/)"),
                # ResponseSchema(
                #     name="MITRE Techniques Description",
                #     description="Offer a concise explanation of the MITRE Techniques ID from the MITRE ATT&CK® framework",
                # ),
                # ResponseSchema(
                #     name="CAPEC Reference URL", description="Include the URL of the Common Attack Pattern Enumeration and Classification (CAPEC) database entry for each threat, linking to its CAPEC page(e.g.,https://capec.mitre.org/data/definitions/1000.html)"),
                # ResponseSchema(
                #     name="NIST Reference",
                #     description="Provide relevant information or recommendations from the National Institute of Standards and Technology (NIST)",
                # )
                # ]
                
                response_schemas = [
                                    ResponseSchema(
                                        name="Threat Name",
                                        description="A descriptive name for each potential threat (e.g., Data Manipulation)"
                                    ),
                                    ResponseSchema(
                                        name="Threat Description",
                                        description="Offer a concise explanation of the potential attack. For example, describe how attackers can manipulate data in given component name due to improper access controls or vulnerabilities in the application using the database."
                                    ),
                                    ResponseSchema(
                                        name="Attack Domain",
                                        description="Specify the category of attack, such as network or application"
                                    ),
                                    ResponseSchema(
                                        name="Countermeasure",
                                        description="Suggest recommendations to mitigate each threat"
                                    ),
                                    ResponseSchema(
                                        name="NIST Reference",
                                        description="Provide relevant information or recommendations from the National Institute of Standards and Technology (NIST)"
                                    ),
                                    ResponseSchema(
                                        name="ASVS Reference",
                                        description="Reference to the OWASP Application Security Verification Standard (ASVS)"
                                    ),
                                    ResponseSchema(
                                        name="OWASP Reference",
                                        description="Reference to the Open Web Application Security Project (OWASP)"
                                    ),
                                    ResponseSchema(
                                        name="SANS Reference",
                                        description="Reference to the SANS Institute, a leading organization in cybersecurity education and training"
                                    ),
                                    ResponseSchema(
                                        name="CIS Reference",
                                        description="Reference to the Center for Internet Security (CIS), a nonprofit organization that provides cybersecurity resources and best practices"
                                    ),
                                    ResponseSchema(
                                        name="MITRE Tactics ID",
                                        description="Specify the corresponding MITRE Tactics ID URL from the MITRE ATT&CK® framework (e.g., https://attack.mitre.org/tactics/TA0043/)"
                                    ),
                                    ResponseSchema(
                                        name="MITRE Tactics Description",
                                        description="Provide a brief description of the MITRE Tactics ID from the MITRE ATT&CK® framework."
                                    ),
                                    ResponseSchema(
                                        name="MITRE Techniques ID",
                                        description="Specify the relevant MITRE Techniques ID URL from the MITRE ATT&CK® framework (e.g., https://attack.mitre.org/techniques/T1548/)"
                                    ),
                                    ResponseSchema(
                                        name="MITRE Techniques Description",
                                        description="Offer a concise explanation of the MITRE Techniques ID from the MITRE ATT&CK® framework"
                                    ),
                                    ResponseSchema(
                                        name="CAPEC Reference URL",
                                        description="Include the URL of the Common Attack Pattern Enumeration and Classification (CAPEC) database entry for each threat, linking to its CAPEC page(e.g.,https://capec.mitre.org/data/definitions/1000.html)"
                                    )
                                
                                ]

                
                # response_schemas = [ResponseSchema(
                #                         name="Threat Name",
                #                         description="A descriptive name for each potential threat (e.g., Data Manipulation, SQL Injection, Insecure Direct Object References, etc.)",
                #                     ),
                #                     ResponseSchema(
                #                         name="Threat Description",
                #                         description="Offer a concise explanation of the potential attack, detailing how attackers can exploit vulnerabilities or weaknesses to achieve their goals. For example, describe how attackers could manipulate data in the given component due to improper access controls or vulnerabilities in the application using the database. Consider referencing relevant attack examples from resources like SANS, OWASP, or MITRE ATT&CK.",
                #                     ),
                #                     ResponseSchema(
                #                         name="Attack Domain",
                #                         description="Specify the category of attack, such as Network, Application, Data, or Physical.",
                #                     ),
                #                     ResponseSchema(
                #                         name="Countermeasure",
                #                         description="Suggest recommendations to mitigate each threat and prevent successful exploitation. Be specific and actionable, referencing best practices and industry standards from organizations like CIS, NIST, or OWASP. Example: 'Implement RBAC and follow the principle of least privilege for data access control. Validate and sanitize all user input to prevent SQL injection.'",
                #                     ),
                #                     ResponseSchema(
                #                         name="MITRE Tactics ID",
                #                         description="Specify the corresponding MITRE Tactics ID URL from the MITRE ATT&CK® framework (e.g., https://attack.mitre.org/tactics/TA0043/), if applicable. Consider using the latest ATT&CK matrix version.",
                #                     ),
                #                     ResponseSchema(
                #                         name="MITRE Tactics Description",
                #                         description="Provide a brief description of the MITRE Tactics ID from the MITRE ATT&CK® framework, if applicable.",
                #                     ),
                #                     ResponseSchema(
                #                         name="MITRE Techniques ID",
                #                         description="Specify the relevant MITRE Techniques ID URL from the MITRE ATT&CK® framework (e.g., https://attack.mitre.org/techniques/T1548/), if applicable. Use the latest ATT&CK matrix version.",
                #                     ),
                #                     ResponseSchema(
                #                         name="MITRE Techniques Description",
                #                         description="Offer a concise explanation of the MITRE Techniques ID from the MITRE ATT&CK® framework, if applicable.",
                #                     ),
                #                     ResponseSchema(
                #                         name="CAPEC Reference URL",
                #                         description="Include the URL of the Common Attack Pattern Enumeration and Classification (CAPEC) database entry for each threat, linking to its CAPEC page (e.g., https://capec.mitre.org/data/definitions/1000.html), if applicable.",
                #                     ),
                #                     ResponseSchema(
                #                         name="NIST Reference",
                #                         description="Provide relevant information or recommendations from the National Institute of Standards and Technology (NIST) Special Publications (SPs) series or other sources, where applicable. For example, cite guidance from NIST SP 800-53 for security controls or SP 800-61 for incident response.",
                #                     ),
                #                     ResponseSchema(
                #                         name="OWASP Reference",
                #                         description="Include the URL of the relevant OWASP Top 10 entry or project page (e.g., https://owasp.org/Top10/), if applicable. Use the latest OWASP Top 10 version.",
                #                     ),
                #                     ResponseSchema(
                #                         name="SANS Reference",
                #                         description="Provide the URL of the corresponding SANS Institute information center page, white paper, or SANS Institute course (e.g., https://www.sans.org/reading-room/whitepapers/incident/securing-web-services-2nd-edition/), if applicable.",
                #                     ),
                #                     ResponseSchema(
                #                         name="CIS Reference",
                #                         description="Include the URL of the relevant Center for Internet Security (CIS) Controls recommendation (e.g., https://www.cisecurity.org/controls/cis-controls-v8/), if applicable.",
                #                     ),
                #                 ]

            
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

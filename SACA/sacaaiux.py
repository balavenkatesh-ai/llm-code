import streamlit as st 
from streamlit_chat import message
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.agents import initialize_agent,Tool
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
#from langchain.agents import create_csv_agent
from langchain.globals import set_debug, set_verbose
from langchain_community.chat_models import ChatOllama
from langchain.tools.retriever import create_retriever_tool
from langchain.tools import tool
from langchain.agents import AgentExecutor
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain_community.llms import Ollama
from langchain_community.llms import GPT4All
import re

set_debug(True)
set_verbose(True)

DB_FAISS_PATH = 'vectorstore/db_faiss'
BASE_URL="http://10.16.1.10:11434"

local_path = ("llama-2-7b-chat.Q5_K_M.gguf")

# Callbacks support token-wise streaming
callbacks = [StreamingStdOutCallbackHandler()]

#llm = Ollama(model="llama2:chat", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

# llm = ChatOllama(model="llama2:13b-chat", temperature=0.2,keep_alive=-1)
# llm = ChatOllama(model="llama2:13b-chat", temperature=0.2,keep_alive=-1)

llm = ChatOllama(model="llama2:chat", temperature=0.1,keep_alive=-1)

# Verbose is required to pass to the callback manager
#llm = GPT4All(model=local_path, callbacks=callbacks, verbose=True)

# st.title("GUARDIAN")

appName = 'MSBR'
st.set_page_config(page_title=appName, page_icon='./static/bot.png', layout="wide")
st.markdown('<div class="banner" style="height:280px"></div>', unsafe_allow_html=True)
loader = CSVLoader(file_path="manifest_data_v1.csv", encoding="utf-8", csv_args={'delimiter': ','})
data = loader.load()
#st.json(data)
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                    model_kwargs={'device': 'cpu'})

db = FAISS.from_documents(data, embeddings)
db.save_local(DB_FAISS_PATH)

retriever = db.as_retriever(search_kwargs={"k":1})
#making the compressor
compressor = LLMChainExtractor.from_llm(llm=llm)
#compressor retriver = base retriever + compressor
compression_retriever = ContextualCompressionRetriever(base_retriever=retriever,
                                                       base_compressor=compressor)

# template = """Answer the question based only on the following context:
# {context}

# Question: {question}
# """
template = """You are an expert at threat modeling. 
Your task is to step back and paraphrase a question to a more generic step-back question, 
which is easier to answer."""

# prompt = ChatPromptTemplate.from_template(template)

memory = ConversationBufferMemory(memory_key="chat_history", output_key='answer', return_messages=False)
# chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever = db.as_retriever(search_type="similarity_score_threshold", 
#                                                 search_kwargs={"score_threshold": 0.3}))
# chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever(search_type="mmr",search_kwargs={"k": 1},
#                                                 chain_type="stuff",memory=memory,verbose=False,
#                                                 combine_docs_chain_kwargs={'prompt': prompt}))
# chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever(search_type="mmr",search_kwargs={"k": 1},
#                                                 verbose=False))
chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=compression_retriever,verbose=True)


def generate_msbr_report_tool(app_name):
    '''
    name = Generate MSBR Report
    description = "Generating MSBR Report based on user given app name"
    '''
    report = f"**Successfully MSBR Report Generated for:** {app_name}"
    return report


retrive_tool = create_retriever_tool(
    compression_retriever,
    name="manifest files",
    description="""Searches and returns documents regarding the Manifest details""",
    
)
#tools = [generate_msbr_report_tool, retrive_tool]
tools = [retrive_tool]

agent_executor = create_conversational_retrieval_agent(llm, tools, verbose=True)

def conversational_chat(query):
    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))
    return result["answer"]

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello ! Ask me anything to generate MSBR Report"]

if 'past' not in st.session_state:
    st.session_state['past'] = [""]

if 'get_app_name' not in st.session_state:
    st.session_state['get_app_name'] = False
    
#container for the chat history
# response_container = st.container()
#container for the user's text input
# container = st.container()
get_app_name = False


if user_input := st.chat_input():
    if re.search(r"generate MSBR report", user_input, re.IGNORECASE) or st.session_state['get_app_name']:
        output = f"Please confirm and type your CI ID only"
        if st.session_state['get_app_name']:
            output = generate_msbr_report_tool(user_input)
            st.session_state['get_app_name'] = False
        else:
            st.session_state['get_app_name'] = True
    else:
        output = conversational_chat(user_input)
    #output = agent_executor.invoke({'input': user_input})
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "ai", "content": output})


    # with response_container:
    # for i in range(len(st.session_state['generated'])):
    #     message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')#, avatar="./static/user-3.png")
    #     message(st.session_state["generated"][i], key=str(i))#, avatar="./static/bot.png")


    # st.markdown(f'<div class="welcome radiant-text"> Hello, {st.session_state["name"]}!</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "ai", "content": "Hi, I am **TIM**, how can I help you today?"}]

for msg in st.session_state.messages:
    if msg["role"] == 'ai':
        (st.chat_message(msg["role"], avatar='./static/bot.png')
            .write(msg["content"]))
    if msg["role"] == 'user':
        (st.chat_message(msg["role"], avatar='./static/user-3.png')
            .write(msg["content"]))
            
def sidebar():
    with st.sidebar:
        logo_column, title_column = st.columns([1, 4])
        with logo_column:
            st.image('./static/bot.png', use_column_width=True)
        with title_column:
            st.title('Guardian Copilot')
    st.sidebar.markdown(
        '<div style="font-size:16px;font-weight:bold;margin-bottom:10px;text-align:center;">Threat Identification & Mitigation Bot</div>',
        unsafe_allow_html=True)

    # Dummy data for now. Update during integration
    st.sidebar.markdown('<hr>', unsafe_allow_html=True)

    # if st.session_state["authentication_status"]:
    #     st.sidebar.button('New Chat', key=reset_conversation)
    # if st.session_state["authentication_status"]:
    #     st.sidebar.markdown(
    #     f'<div class="sidebar-nav"><ul><li>{settingsIcon}<a href="">Settings</a></li><li>{deleteIcon}<a href="">Clear conversations</a></li><li>{faqIcon}<a href="">Updates & FAQ</a></li></ul></div>',
    #     unsafe_allow_html=True)
    #     authenticator.logout("&nbsp;&nbsp;&nbsp;logout&nbsp;&nbsp;&nbsp;", location="sidebar")
    # return None

def styling():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    return None            
styling()
sidebar()            

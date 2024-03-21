# 004_prompt_conversational_chat.md

## prompt
As an advanced programmer in Python using Langchain, Chroma and Streamlit, can you rewrite the Python code below and fix it so the user can chat with a Chroma DB named "chroma_db_conversational_chat"



#%% ---------------------------------------------  IMPORTS  ----------------------------------------------------------#
# Import for reading file
import pathlib
import os
import time
import datetime
import tempfile
from PyPDF2 import PdfReader
import nbformat
import docx2txt

# specific Ollama import
import ollama


# Streamlit Imports
import streamlit as st

# LangChain Imports
# from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Langchain Imports
# from langchain.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chains import LLMChain
from langchain.chains import ConversationalRetrievalChain

# Mistral Imports
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.embeddings import OllamaEmbeddings

# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

#%% --------------------------------------------  FUNCTIONS  ---------------------------------------------------------#
def build_prompt(template_num="template_1"):
    '''This function builds and returns a chosen prompt for a RAG Application with context and a normal LLM Run without'''

    template_1 = """You are a helpful chatbot. You answer the questions of the users giving a lot of details based on what you find in the context.
    You are to act as though you're having a conversation with a human.
    You are only able to answer questions, guide and assist, and provide recommendations to users. You cannot perform any other tasks outside of this.
    Your tone should be professional and friendly.
    Your purpose is to answer questions people might have, however if the question is unethical you can choose not to answer it.
    Your responses should always be one paragraph long or less.
    Context: {context}
    Question: {question}
    Helpful Answer:"""

    template_2 = """You are a helpful chatbot.  You answer the questions of the users giving a lot of details based on what you find in the context.
    Your responses should always be one paragraph long or less.
    Question: {question}
    Helpful Answer:"""

    if template_num == "template_1":
        prompt = PromptTemplate(input_variables=["context", "question"], template=template_1)
        return prompt

    elif template_num == "template_2":
        prompt = PromptTemplate(input_variables=["question"], template=template_2)
        return prompt

    else:
        st.write("Please choose a valid template")

def chat_res_generator():
    
        # Mistral Settings
        embeddings_open = OllamaEmbeddings(model="mistral")
        llm_open = Ollama(model="mistral", temperature=0.2, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

        knowledge_base = Chroma(persist_directory="./chroma_db_conversational_chat", embedding_function=embeddings_open)
        docs = knowledge_base.similarity_search(st.session_state.prompt)


        llm = Ollama(model="mistral", temperature=0,
                 callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

        qa_chain = RetrievalQA.from_chain_type(llm_open, chain_type="stuff",
                                           retriever=knowledge_base.as_retriever(search_kwargs={"k": 2}),
                                           chain_type_kwargs={"prompt": build_prompt("template_1")})
        answer = qa_chain({"query": st.session_state.prompt})
        message = answer["result"]
        return message
#%% --------------------------------------------  APP  ---------------------------------------------------------#           
st.title("RAG Chatbot Streamlit")


# init prompt
if "prompt" not in st.session_state:
    st.session_state["prompt"] = ""

# initialize history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

 # Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # add latest message to history in format {role, content}
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message = st.write_stream(chat_res_generator())
        st.session_state["messages"].append({"role": "assistant", "content": prompt})



## output_chatgpt

# Importing necessary libraries
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Initializing Streamlit app
st.title("Conversational Chat with Chroma DB")

# Checking and initializing session state variables
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "prompt" not in st.session_state:
    st.session_state["prompt"] = ""

# Defining function to generate chatbot responses
def chat_res_generator(prompt):
    # Initializing Ollama model
    llm = Ollama(model="mistral", temperature=0.2, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    
    # Initializing Chroma DB
    knowledge_base = Chroma(persist_directory="./chroma_db_conversational_chat")
    
    # Performing similarity search in the Chroma DB
    docs = knowledge_base.similarity_search(prompt)
    
    # Initializing QA chain
    qa_chain = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=knowledge_base.as_retriever(search_kwargs={"k": 2}))
    
    # Getting response from QA chain
    answer = qa_chain({"query": prompt})
    message = answer["result"]
    return message

# Displaying chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.container():
        st.write(f"{message['role']}: {message['content']}")

# Accepting user input
user_input = st.text_input("You:", key="user_input")

# Handling user input
if st.button("Send"):
    # Adding user input to session state messages
    st.session_state["messages"].append({"role": "User", "content": user_input})
    
    # Generating bot response
    bot_response = chat_res_generator(user_input)
    
    # Adding bot response to session state messages
    st.session_state["messages"].append({"role": "Bot", "content": bot_response})

# Resetting session state
if st.button("Reset Chat"):
    st.session_state["messages"] = []
    st.session_state["prompt"] = ""


## output_mistral




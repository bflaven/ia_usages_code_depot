#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name llm_query_poc python=3.9.13
conda info --envs
source activate llm_query_poc
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n llm_query_poc

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

python -m pip install python-dotenv
python -m pip install langchain-openai

python -m pip install nbformat
python -m pip install docx2txt
python -m pip install chromadb

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages_code_depot/code_rag_chatbot_with_streamlit

# LAUNCH the file
streamlit run 001_rag_chatbot_with_streamlit.py


"""




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


# Function to generate chatbot response
# def generate_response(prompt):
#     knowledge_base = Chroma(persist_directory="./chroma_db_conversational_chat")
#     llm = Ollama(model="mistral", temperature=0.2)

#     qa_chain = RetrievalQA.from_chain_type(llm, chain_type="stuff",
#                                            retriever=knowledge_base.as_retriever(search_kwargs={"k": 2}),
#                                            chain_type_kwargs={"prompt": build_prompt("template_1")})
#     answer = qa_chain({"query": prompt})
#     return answer["result"]

def chat_res_generator():
    

    # stream = ollama.chat(
    #     model=st.session_state["model"],
    #     messages=st.session_state["messages"],
    #     stream=True,
    # )
    # for chunk in stream:
    #     yield chunk["message"]["content"]

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







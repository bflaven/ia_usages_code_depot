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

# install
python -m pip install python-dotenv
python -m pip install langchain-openai
python -m pip install nbformat
python -m pip install docx2txt
python -m pip install chromadb
python -m pip install python-docx

#required
python -m pip install streamlit
python -m pip install chroma

python -m pip uninstall textract



# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_using_flowiseai/_bf_conversational_chat/

# LAUNCH the file
streamlit run 007_python_query_chroma_app_streamlit.py

"""

#%% ---------------------------------------------  IMPORTS  ----------------------------------------------------------#
import time
import datetime
import tempfile
from PyPDF2 import PdfReader
import nbformat
import docx2txt
import os
import pandas as pd
# Import for reading file
import pathlib
from pathlib import Path
import docx
import csv

# # required to create DB
# from chroma import ChromaDB

# Streamlit Imports
import streamlit as st

# LangChain Imports
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Langchain Imports
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


# LangChain Imports
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts.prompt import PromptTemplate

# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# "Mal nommer les choses, c'est ajouter au malheur du monde !" Albert Camus


#%% ---------------------------------------------  APP  ----------------------------------------------------------#


class ConversationalChatApp:
    def __init__(self):
        # self.db_name = "chroma_db_conversational_chat"
        # self.template_1 = "Answer the following question based on the context provided: {question}"
        # self.qa_chain = RetrievalQA.from_chain_type(llm=None, chain_type="stuff", retriever=None, return_source_documents=True)

    def check_database(self):
        # if os.path.exists(self.db_name):
        #     st.write(f"The database '{self.db_name}' already exists.")
        # else:
        #     st.write(f"The database '{self.db_name}' does not exist.")

    def create_database(self):
        # if not os.path.exists(self.db_name):
        #     st.write(f"Creating the database '{self.db_name}'...")
        #     self.vectorstore = Chroma(persist_directory=self.db_name, embedding_function=embeddings)
        #     st.write(f"The database '{self.db_name}' has been successfully created.")
        # else:
        #     st.write(f"The database '{self.db_name}' already exists. Loading the database...")
        #     self.vectorstore = Chroma(persist_directory=self.db_name, embedding_function=embeddings)

    def ingest_documents(self, files):
        # for file in files:
        #     file_extension = os.path.splitext(file.name)[1]

        #     if file_extension == ".pdf":
        #         loader = PyPDFLoader(file)
        #     elif file_extension in [".docx", ".doc"]:
        #         loader = UnstructuredFileLoader(file, mode="elements")
        #     elif file_extension in [".txt"]:
        #         loader = TextLoader(file)
        #     else:
        #         st.write(f"Unsupported file format: {file_extension}")
        #         continue

        #     documents = loader.load()
        #     self.vectorstore.add_documents(documents)
        #     st.write(f"Ingested {len(documents)} documents from {file.name}.")

    def request_database(self, prompt):
        # result = self.qa_chain.run(input_documents=self.vectorstore, question=prompt, chain_type_kwargs={"prompt": self.template_1})
        # st.write(result)

def main():
    app = ConversationalChatApp()

    st.title("Conversational Chat App")

    tab1, tab2, tab3 = st.tabs(["Database", "Request", "Ingest Documents"])

    with tab1:
        st.header("Tab 1: Database Management")
        # app.check_database()
        if st.button("Create Database"):
            # app.create_database()

    with tab3:
        st.header("Tab 3: Ingest Documents")
        # files = st.file_uploader("Upload documents", type=["pdf", "docx", "txt"], accept_multiple_files=True)
        if st.button("Ingest Documents") and files:
            # app.ingest_documents(files)

    with tab2:
        st.header("Tab 2: Request Database")
        # prompt = st.text_input("Enter your prompt:")
        if st.button("Request") and prompt:
            # app.request_database(prompt)

if __name__ == "__main__":
    main()


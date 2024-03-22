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
cd /Users/brunoflaven/Documents/03_git/ia_usages_code_depot/code_python_query_chroma_app_streamlit/

# LAUNCH the file
streamlit run 006_python_query_chroma_app_streamlit.py

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
class ChromaApp:
    def __init__(self):
        self.db_name = "chroma_db_conversational_chat"
        self.db_path = f"./{self.db_name}.db"
        self.db_created = os.path.exists(self.db_path)
        self.db = Chroma(self.db_path)

    def create_database_tab(self):
        st.title("Create Chroma Database")
        if self.db_created:
            st.write(f"Database '{self.db_name}' already exists.")
        else:
            self.db.create_database()
            st.write(f"Database '{self.db_name}' created successfully.")

    def ingest_documents_tab(self):
        st.title("Ingest Documents to Database")
        st.write("Upload documents (.pdf, .docx, .txt) to store in the database.")

        uploaded_files = st.file_uploader("Upload Files", type=["pdf", "docx", "txt"], accept_multiple_files=True)

        if uploaded_files:
            for file in uploaded_files:
                content = file.getvalue().decode("utf-8")
                self.db.store_document(content)
                st.write(f"File '{file.name}' ingested successfully.")

    def request_database_tab(self):
        st.title("Request Database")
        st.write("Enter your request template to query the database.")

        template_1 = st.text_input("Enter Template 1")

        if st.button("Submit"):
            results = self.db.query(template_1)
            st.write("Results:")
            st.write(results)

    def run(self):
        st.sidebar.title("Chroma App")
        tab_selection = st.sidebar.radio("Select Tab", ["Create Database", "Ingest Documents", "Request Database"])

        if tab_selection == "Create Database":
            self.create_database_tab()
        elif tab_selection == "Ingest Documents":
            self.ingest_documents_tab()
        elif tab_selection == "Request Database":
            self.request_database_tab()

if __name__ == "__main__":
    app = ChromaApp()
    app.run()


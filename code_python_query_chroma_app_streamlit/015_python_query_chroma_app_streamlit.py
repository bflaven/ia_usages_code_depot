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
pip uninstall textract

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_using_flowiseai/_bf_conversational_chat/

# LAUNCH the file
streamlit run 015_python_query_chroma_app_streamlit.py

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
import io

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
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts.prompt import PromptTemplate


# Required for streamlit app
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredFileLoader


# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


class ChromaChatApp:
    def __init__(self):
        self.user_input_source = ""
        self.user_input_prompt = ""
        self.result = ""

    def build_prompt(self, template_num="template_1"):
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
            print("Please choose a valid template")

    def file_uploader(self, user_input_source):
        file_extension = os.path.splitext(user_input_source)[1][1:]
        text = ""

        if file_extension in ["txt"]:
            try:
                with open(user_input_source, "r", encoding="utf-8") as f:
                    text = f.read()
                    text += "\n"  # Append a newline character at the end of the text
            except Exception as e:
                print(f"Error reading {file_extension.upper()} file:", e)

        elif file_extension in ["pdf"]:
            try:
                text = extract_text_pdf(user_input_source)
            except Exception as e:
                print(f"Error reading {file_extension.upper()} file:", e)

        elif file_extension in ["docx"]:
            try:
                doc = docx.Document(user_input_source)
                full_text = []
                for para in doc.paragraphs:
                    full_text.append(para.text)
                    text = '\n'.join(full_text)
            except Exception as e:
                print(f"Error reading {file_extension.upper()} file:", e)

        elif file_extension in ["html", "css", "py"]:
            try:
                with open(user_input_source, "r") as f:
                    file_content = f.read()
                    text += file_content + "\n"
            except Exception as e:
                print(f"Error reading {file_extension.upper()} file:", e)

        elif file_extension == "csv":
            try:
                with open(user_input_source, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        text += ','.join(row) + '\n'
            except Exception as e:
                print(f"Error reading {file_extension.upper()} file:", e)

        return text

    def insert_db(self, text):
        chunks = CharacterTextSplitter(chunk_size=200, chunk_overlap=50).split_text(text)
        knowledge_base = Chroma.from_texts(chunks, OllamaEmbeddings(model="mistral"), persist_directory="./chroma_db_conversational_chat")
        prompt = self.build_prompt("template_1")
        qa_chain = RetrievalQA.from_chain_type(Ollama(model="mistral", temperature=0.2, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])), chain_type="stuff", retriever=knowledge_base.as_retriever(), chain_type_kwargs={"prompt": prompt})
        answer = qa_chain({"query": self.user_input_prompt})
        self.result = answer["result"]

    def run(self):
        st.title("Chroma Chat App")
        # self.user_input_source = st.text_input("Enter the source file path:")
        # File uploader
        user_input_source = st.file_uploader("Upload a document", type=["txt", "pdf", "docx", "html", "css", "py", "csv"])
        
        self.user_input_prompt = st.text_input("Enter the prompt:")
        
        if st.button("Submit"):
            if self.user_input_source and self.user_input_prompt:
                text = self.file_uploader(self.user_input_source)
                self.insert_db(text)
                st.write("Result:")
                st.write(self.result)

if __name__ == "__main__":
    app = ChromaChatApp()
    app.run()


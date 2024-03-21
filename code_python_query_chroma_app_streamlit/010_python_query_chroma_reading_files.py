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
python -m pip install python-docx


# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_using_flowiseai/_bf_conversational_chat/

# LAUNCH the file
python 010_python_query_chroma_reading_files.py


# caution with errors for loading in langchain
- Chroma
- Docx2txtLoader
- OllamaEmbeddings

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
from pathlib import Path
import docx
import csv

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

# LangChain Imports
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts.prompt import PromptTemplate

# Import for reading file
import pathlib

# Text treatment

# for vroux_transcript.txt
# PATH_TO_SOURCE = "_data/sample_transcript.txt"
# user_input= "Who is Carter Gottwin Woodson?"

# for robert_badinter_small_bio.txt
# PATH_TO_SOURCE = "_data/robert_badinter_small_bio.txt"
# user_input= "Is it about Robert Badinter? Where Robert Badinter was born and what is the \"Parti socialiste\"?"

# for robert_badinter_small_bio.txt
# PATH_TO_SOURCE = "_data/source_african_football_2.txt"
# user_input= "Who is Julien Mette and What is his nationality?"

# just query 
# PATH_TO_SOURCE = "_data/empty_file.txt"
# user_input= "What is BFA?"

# without CV, does not know
# user_input= "What is HECUBE?"

# should know
# PATH_TO_SOURCE = "_data/empty_file.txt"
# user_input= "Who is Nabil Bentaleb?"

# should NOT know
# PATH_TO_SOURCE = "_data/empty_file.txt"
# user_input= "Who is Dylan Bron?"

# should NOT know
# PATH_TO_SOURCE = "_data/empty_file.txt"
# user_input= "Who is Dylan Bron?"

# should know
# user_input_source = "_data/source_african_football_3.txt"
# user_input_prompt= "Who is Dylan Bron?"

# user_input_source = "_data/empty_file.txt"
# user_input_prompt= "Who is Houssem Habbassi?"
# user_input_prompt= "Who is Emmanuel Ndoumbe Bosso?"

# user_input_source = "_data/empty_file.txt"
# user_input_prompt= "Who is Houssem Habbassi?"
# user_input_prompt= "Who is Emmanuel Ndoumbe Bosso?"


# user_input_source = "_data/source_african_football_4.txt"
# user_input_source = "_data/fake_doc.docx"
# user_input_source = "_data/fake_pdf.pdf"
# user_input_source = "_data/people_basket_en_full_google_trends.csv"
# user_input_source = "_data/strings.en.csv"
# user_input_source = "_data/sample_html_flaven_fr.html"

# user_input_source = "_data/source_african_football_3.txt"
# user_input_prompt= "Who is Dylan Bron?"

# Text treatment

# "Mal nommer les choses, c'est ajouter au malheur du monde !" Albert Camus

user_input_source = "_data/source_african_football_3.txt"
user_input_prompt= "Who is Houssem Habbassi?"


#%% --------------------------------------------  INIT LLM  ---------------------------------------------------------#
# Mistral Settings
embeddings_open = OllamaEmbeddings(model="mistral")
llm_open = Ollama(model="mistral", temperature=0.2, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))


#%% --------------------------------------------  FUNCTIONS  ---------------------------------------------------------#
# Create your own prompt by using the template below.
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
        print("Please choose a valid template")

def file_uploader(user_input_source):
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
            # --- Temporary file save ---
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(open(user_input_source, 'rb').read())
                temp_file_path = temp_file.name
                # --- reading PDF content ---
                with open(temp_file_path, "rb") as f:
                    pdf = PdfReader(f)
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        text += page_text + "\n"  # Append the text of each page to the list

        except Exception as e:
            print(f"Error reading {file_extension.upper()} file:", e)

    elif file_extension in ["docx"]:
            try:
                # --- Temporary file save ---
                with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
                    temp_file.write(open(user_input_source, 'rb').read())
                    temp_file_path = temp_file.name
                    doc = docx.Document(temp_file_path)
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
            # Check if the file exists
            if not os.path.exists(user_input_source):
                print(f"File {user_input_source} not found.")
                return

            # Create a temporary file to store extracted content
            temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)

            try:
                # Open the CSV file
                with open(user_input_source, 'r') as csv_file:
                    # Create a CSV reader object
                    # csv_reader = csv.reader(csv_file)
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    header = next(csv_reader, None)  # Skip header row, if any
                    # Iterate over each row in the CSV file
                    for row in csv_reader:
                        # Write each row to the temporary file
                        temp_file.write(','.join(row) + '\n')

                # print("Content extracted successfully.")
                
                # Move the cursor to the beginning of the file
                temp_file.seek(0)
                
                # Read and print the content of the temporary file
                # print("Extracted Content:")
                # print(temp_file.read())
                text = temp_file.read()
            except Exception as e:
                print(f"Error occurred while extracting content: {str(e)}")
            finally:
                # Close the temporary file
                temp_file.close()
                # Remove the temporary file
                os.unlink(temp_file.name)

    # result
    return text

def insert_db (text):
        # Read the file
        file_path = pathlib.Path(user_input_source)
        text = file_path.read_text()

        # Initialize text splitter
        text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
        chunks = text_splitter.split_text(text)

        # Initialize Chroma
        knowledge_base = Chroma.from_texts(chunks, embeddings_open, persist_directory="./chroma_db_conversational_chat")

        # Initialize prompt
        prompt = build_prompt("template_1")

        # Initialize RetrievalQA
        qa_chain = RetrievalQA.from_chain_type(llm_open, chain_type="stuff", retriever=knowledge_base.as_retriever(), chain_type_kwargs={"prompt": prompt})

        # Get answer
        answer = qa_chain({"query": user_input_prompt})
        result = answer["result"]

        print('\n')

# ------------------- INSERT ----------------- #
# file_uploader(user_input_source)
# insert_db (user_input_source)




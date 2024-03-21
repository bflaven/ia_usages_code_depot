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

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_using_flowiseai/ollama_pdfchat_streamlit

# LAUNCH the file
streamlit run 016_python_query_chroma_app_streamlit.py

# INSTALL
python -m pip install streamlit


Chroma
Docx2txtLoader
OllamaEmbeddings



"""

from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
# from langchain.llms import Ollama
from langchain_community.llms import Ollama
from langchain.embeddings.ollama import OllamaEmbeddings
# from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import streamlit as st
import os
import time


# model="mistral:instruct"
# model="mistral:lastest"
# model="mistral"

if not os.path.exists('files'):
    os.mkdir('files')

if not os.path.exists('jj'):
    os.mkdir('jj')

if 'template' not in st.session_state:
    st.session_state.template = """You are a knowledgeable chatbot, here to help with questions of the user. Your tone should be professional and informative.

    Context: {context}
    History: {history}

    User: {question}
    Chatbot:"""
if 'prompt' not in st.session_state:
    st.session_state.prompt = PromptTemplate(
        input_variables=["history", "context", "question"],
        template=st.session_state.template,
    )
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True,
        input_key="question")
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = Chroma(persist_directory='jj',
                        embedding_function=OllamaEmbeddings(
                            model="mistral")
                        )
if 'llm' not in st.session_state:
    st.session_state.llm = Ollama(base_url="http://localhost:11434",
                model="mistral",
                verbose=True,
                callback_manager=CallbackManager(
                    [StreamingStdOutCallbackHandler()]),
                )

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("PDF Chatbot")

# Upload files
# uploaded_file = st.file_uploader("Upload your files", type='pdf')
uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])
       


for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["message"])




if uploaded_file is not None:
    file_extension = os.path.splitext("files/"uploaded_file.name)[1][1:]
    # file_extension = os.path.isfile("files/"+uploaded_file.name+".pdf")
    text = ""

    if file_extension in ["txt"]:
        try:
            with open(uploaded_file.name, "r", encoding="utf-8") as f:
                text = f.read()
                text += "\n"  # Append a newline character at the end of the text
        except Exception as e:
            print(f"Error reading {file_extension.upper()} file:", e)

    elif file_extension in ["pdf"]:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name
                with open(temp_file_path, "rb") as f:
                    pdf = PdfReader(f)
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        text += page_text + "\n"  # Append the text of each page to the list

        except Exception as e:
            print(f"Error reading {file_extension.upper()} file:", e)

    elif file_extension in ["docx"]:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
                temp_file.write(uploaded_file.read())
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
            with open(uploaded_file.name, "r") as f:
                file_content = f.read()
                text += file_content + "\n"

        except Exception as e:
            print(f"Error reading {file_extension.upper()} file:", e)

    elif file_extension == "csv":
        try:
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
                temp_file.write(uploaded_file.read().decode('utf-8'))
                temp_file_path = temp_file.name
                with open(temp_file_path, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        text += ','.join(row) + '\n'

        except Exception as e:
            print(f"Error occurred while extracting content: {str(e)}")

    if text:
        st.code(text)
    else:
        st.write("No text to display.")

else:
    st.write("Please upload a file...")

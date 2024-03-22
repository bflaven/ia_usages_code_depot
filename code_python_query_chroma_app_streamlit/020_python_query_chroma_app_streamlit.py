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
cd /Users/brunoflaven/Documents/03_git/ia_usages_code_depot/code_python_query_chroma_app_streamlit

# LAUNCH the file
streamlit run 019_python_query_chroma_app_streamlit.py

# INSTALL
python -m pip install streamlit


Chroma
Docx2txtLoader
OllamaEmbeddings



"""

#%% ---------------------------------------------  IMPORTS  ----------------------------------------------------------#
import time
import datetime
import tempfile
from PyPDF2 import PdfReader
import nbformat
import docx2txt

# Streamlit Imports
import streamlit as st
from streamlit_chat import message

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
# from langchain.llms import Ollama
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.embeddings import OllamaEmbeddings
from langchain_community.embeddings import OllamaEmbeddings

# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


# Mistral Settings
embeddings_open = OllamaEmbeddings(model="mistral")
llm_open = Ollama(model="mistral", temperature=0.2,
                         callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))



#%% --------------------------------------------  FILE UPLOADER  -----------------------------------------------------#
def file_uploader():
    ''' This function handles the file upload in the streamlit sidebar and returns the text of the file.'''
    # ------------------ SIDEBAR ------------------- #
    st.sidebar.subheader("File Uploader:")
    uploaded_files = st.sidebar.file_uploader("Choose files",
                                              type=["txt", "html", "css", "py", "pdf", "ipynb", "docx", "csv"],
                                              accept_multiple_files=True)
    st.sidebar.metric("Number of files uploaded", len(uploaded_files))

    # ------------------- FILE HANDLER ------------------- #
    text = ""  # Define text variable here
    if uploaded_files:

        file_index = st.sidebar.selectbox("Select a file to display", options=[f.name for f in uploaded_files])
        selected_file = uploaded_files[[f.name for f in uploaded_files].index(file_index)]

        file_extension = selected_file.name.split(".")[-1]

        if file_extension in ["pdf"]:
            try:
                # --- Temporary file save ---
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(selected_file.getvalue())
                    temp_file_path = temp_file.name

                # --- Writing PDF content ---
                with st.expander("Document Expander (Press button on the right to fold or unfold)", expanded=True):
                    st.subheader("Uploaded Document:")
                    with open(temp_file_path, "rb") as f:
                        pdf = PdfReader(f)
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            text += page_text + "\n"  # Append the text of each page to the list
                            st.write(page_text)

            except Exception as e:
                st.write(f"Error reading {file_extension.upper()} file:", e)

        elif file_extension in ["docx"]:
            try:
                # --- Temporary file save ---
                with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
                    temp_file.write(selected_file.getvalue())
                    temp_file_path = temp_file.name

                # --- Writing PDF content ---
                with st.expander("Document Expander (Press button on the right to fold or unfold)", expanded=True):
                    st.subheader("Uploaded Document:")
                    with open(temp_file_path, "rb") as f:
                        docx = Docx2txtLoader(temp_file_path)
                        pages = docx.load()
                        for page in pages:
                            text += page.page_content + "\n"

                        st.write(text)

            except Exception as e:
                st.write(f"Error reading {file_extension.upper()} file:", e)

        elif file_extension in ["html", "css", "py", "txt"]:
            try:
                file_content = selected_file.getvalue().decode("utf-8")

                # --- Display the file content as code---
                with st.expander("Document Expander (Press button on the right to fold or unfold)", expanded=True):
                    st.subheader("Uploaded Document:")
                    st.code(file_content, language=file_extension)
                    text += file_content + "\n"

            except Exception as e:
                st.write(f"Error reading {file_extension.upper()} file:", e)

        # elif file_extension == "ipynb":
        #     try:
        #         nb_content = nbformat.read(selected_file, as_version=4)
        #         nb_filtered = [cell for cell in nb_content["cells"] if cell["cell_type"] in ["code", "markdown"]]
        #         nb_cell_content = [cell["source"] for cell in nb_filtered]

        #         # --- Display the file content as code---
        #         with st.expander("Document Expander (Press button on the right to fold or unfold)", expanded=True):
        #             st.subheader("Uploaded Document:")
        #             for cell in nb_filtered:
        #                 if cell["cell_type"] == "code":
        #                     st.code(cell["source"], language="python")
        #                 elif cell["cell_type"] == "markdown":
        #                     st.markdown(cell["source"])
        #                     text += cell["source"] + "\n"

        #     except Exception as e:
        #         st.write(f"Error reading {file_extension.upper()} file:", e)

        # elif file_extension == "csv":
        #         # use tempfile because CSVLoader only accepts a file_path
        #         with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        #             tmp_file.write(selected_file.getvalue())
        #             tmp_file_path = tmp_file.name

        #         loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={
        #             'delimiter': ','})
        #         text = loader.load()

    return text

#%% --------------------------------------------  FUNCTIONS  ---------------------------------------------------------#
# Create your own prompt by using the template below.
def build_prompt(template_num="template_1"):
    '''This function builds and returns a choosen prompt for a RAG Application with context and a normal LLM Run without'''

    template_1 = """You are a helpful chatbot, created by the RSLT Team. You answer the questions of the customers giving a lot of details based on what you find in the context.
    You are to act as though you're having a conversation with a human.
    You are only able to answer questions, guide and assist, and provide recommendations to users. You cannot perform any other tasks outside of this.
    Your tone should be professional and friendly.
    Your purpose is to answer questions people might have, however if the question is unethical you can choose not to answer it.
    Your responses should always be one paragraph long or less.
    Context: {context}
    Question: {question}
    Helpful Answer:"""

    template_2 = """You are a helpful chatbot, created by the RSLT Team.  You answer the questions of the customers giving a lot of details based on what you find in the context. 
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


# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
# ---------------------- for message -------------------- #
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["message"])

#%% --------------------------------------------  PAGE CONTENT  ------------------------------------------------------#
st.set_page_config(page_title="Home", layout="wide")
# st.sidebar.image("rslt_logo_dark_mode.png", width=200)
st.sidebar.title("")
# ---------------------- MAIN PAGE -------------------- #
st.sidebar.title("Choose application type and settings:")
st.subheader("Mistral AI - Chat, RAG and Knowledge Base Application")

# ---------------------- VECTOR DB -------------------- #
# Selectbox for database
application_type = st.sidebar.selectbox("Select an application", options=["Intro", "Mistral RAG", "Mistral Knowledge Base"])

if application_type == "Mistral RAG" or application_type == "Mistral Knowledge Base":
    vector_db_path_selector = st.sidebar.selectbox("Select a database", options=["./test_chroma_db_1/", "./test_chroma_db_2/" ])
    collection_selector = st.sidebar.selectbox("Select a collection", options=["collection_1", "collection_2", "collection_3"])

# ---------------------- FILE UPLOADER -------------------- #
if application_type == "Intro":
    st.write ('Hello')
    user_input=""

# ---------------------- FILE UPLOADER -------------------- #
if application_type == "Mistral RAG":
    text = file_uploader()


current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

# --------------------- USER INPUT --------------------- #
if application_type == "Mistral RAG" or application_type == "Mistral Knowledge Base":
    user_input = st.text_area("Your prompt: ")
    st.button('Send')

# ------------------- GENERAL -------------------- #
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


# ------------------- TRIGGERED -------------------- #
if user_input:

    if user_input:
        transcript = user_input

    if 'transcript' not in st.session_state:
        st.session_state.transcript = transcript
    else:
        st.session_state.transcript = transcript

    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{"role": "user", "content": transcript}]
    else:
        st.session_state['messages'].append({"role": "user", "content": transcript})
        st.write('Send is clicked')
        # ------------------- TRANSCRIPT ANSWER ----------------- #
        with st.spinner("Fetching answer ..."):

            # ------------------- RAG CHAIN ----------------- #
            if text is not None:
                text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
                chunks = text_splitter.split_text(text)

                knowledge_base = Chroma.from_texts(chunks, embeddings_open, persist_directory="./chroma_db")
                docs = knowledge_base.similarity_search(st.session_state.transcript)

                st.write(f"Found {len(docs)} chunks.")

                llm = Ollama(model="mistral", temperature=0,
                             callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

                text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
                chunks = text_splitter.split_text(text)

                knowledge_base = Chroma.from_texts(chunks, embeddings_open, persist_directory="./chroma_db")
                docs = knowledge_base.similarity_search(st.session_state.transcript)

                st.write(f"Found {len(docs)} chunks.")

                llm = Ollama(model="mistral", temperature=0,
                             callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

                qa_chain = RetrievalQA.from_chain_type(llm_open, chain_type="stuff",
                                                       retriever=knowledge_base.as_retriever(),
                                                       chain_type_kwargs={"prompt": build_prompt("template_1")})
                answer = qa_chain({"query": st.session_state.transcript})
                result = answer["result"]

                
                st.markdown(result)
                


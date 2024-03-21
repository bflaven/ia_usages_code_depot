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
streamlit run 014_python_query_chroma_app_streamlit.py

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

if 'retriever' not in st.session_state:
    # Initialize your retriever attribute here
    st.session_state.retriever = None  # or initialize it to your appropriate retriever instance

class ChatApp:
    def __init__(self):
        self.chat_history = []



    def initialize_environment(self):
        # Initialize necessary directories and session states
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
        
        if 'retriever' not in st.session_state:
            st.session_state.retriever = RetrievalQA.from_chain_type(
                llm=st.session_state.llm,
                chain_type='stuff',
                retriever=st.session_state.retriever,
                verbose=True,
                chain_type_kwargs={
                    "verbose": True,
                    "prompt": st.session_state.prompt,
                    "memory": st.session_state.memory,
                }
            )

    def upload_file(self):
        # Upload a file
        uploaded_file = st.file_uploader("Upload your file", type=['pdf', 'txt', 'docx'])

        if uploaded_file is not None:
            # Check if the file is uploaded successfully
            try:
                self.process_file(uploaded_file)
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

    def process_file(self, uploaded_file):
        # Process the uploaded file
        file_path = os.path.join("files", uploaded_file.name)

        if not os.path.isfile(file_path):
            with st.status("Analyzing your document..."):
                bytes_data = uploaded_file.read()
                with open(file_path, "wb") as f:
                    f.write(bytes_data)

                if uploaded_file.type == 'pdf':
                    self.process_pdf(file_path)
                elif uploaded_file.type == 'txt':
                    self.process_text(file_path)
                elif uploaded_file.type == 'docx':
                    self.process_docx(file_path)
        else:
            st.warning("File already processed")

    def process_pdf(self, file_path):
        # Process PDF file
        loader = PyPDFLoader(file_path)
        data = loader.load()

        # Initialize text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200,
            length_function=len
        )
        all_splits = text_splitter.split_documents(data)

        # Create and persist the vector store
        st.session_state.vectorstore = Chroma.from_documents(
            documents=all_splits,
            embedding=OllamaEmbeddings(model="mistral")
        )
        st.session_state.vectorstore.persist()

    def process_text(self, file_path):
        # Process text file
        # Add your text file processing logic here
        pass

    def process_docx(self, file_path):
        # Process docx file
        # Add your docx file processing logic here
        pass

    def chat_interaction(self):
        # Chat input
        user_input = st.text_input("You:")
        if user_input:
            user_message = {"role": "user", "message": user_input}
            self.chat_history.append(user_message)

            with st.spinner("Assistant is typing..."):
                response = st.session_state.retriever(user_input)

            chatbot_message = {"role": "assistant", "message": response['result']}
            self.chat_history.append(chatbot_message)

            self.display_chat_messages()

    def display_chat_messages(self):
        # Display chat messages
        for message in self.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["message"])

def main():
    st.title("Chroma Chat App")
    chat_app = ChatApp()
    chat_app.initialize_environment()

    if st.session_state.chat_history:
        chat_app.display_chat_messages()
    else:
        st.write("Please upload a file.")
    
    chat_app.upload_file()
    chat_app.chat_interaction()

if __name__ == "__main__":
    main()

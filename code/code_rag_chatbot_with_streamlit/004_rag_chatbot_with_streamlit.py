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
streamlit run 004_rag_chatbot_with_streamlit.py


"""



# Importing necessary libraries
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter

# Initializing Streamlit app
st.title("Conversational Chat with Chroma DB")

# Checking and initializing session state variables
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "prompt" not in st.session_state:
    st.session_state["prompt"] = ""

# Defining function to generate chatbot responses
def chat_res_generator(prompt):

    # Initializing Ollama model and Mistral Settings
    embeddings_open = OllamaEmbeddings(model="mistral")
    llm = Ollama(model="mistral", temperature=0.2, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

    # fake
    text = "Lorem ipsum"

    # Initialize text splitter
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    chunks = text_splitter.split_text(text)

    # Initialize Chroma
    knowledge_base = Chroma.from_texts(chunks, embeddings_open, persist_directory="./chroma_db_conversational_chat")

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






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
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_using_flowiseai/_bf_conversational_chat/rag_chatbot_with_streamlit/

# LAUNCH the file
streamlit run 003_rag_chatbot_with_streamlit.py


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

    # Initializing embedding function
    # embeddings_open = OllamaEmbeddings(model="mistral", chunk_size=1)

    # Initializing Chroma DB with the embedding function
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






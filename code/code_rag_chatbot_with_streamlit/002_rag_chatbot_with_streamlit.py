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
streamlit run 002_rag_chatbot_with_streamlit.py


"""



# Import necessary libraries
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Function to build prompt
def build_prompt(template_num="template_1"):
    templates = {
        "template_1": "You are a helpful chatbot. You answer the questions of the users giving a lot of details based on what you find in the context. Your responses should always be one paragraph long or less. Context: {context} Question: {question} Helpful Answer:",
        "template_2": "You are a helpful chatbot. You answer the questions of the users giving a lot of details based on what you find in the context. Your responses should always be one paragraph long or less. Question: {question} Helpful Answer:"
    }
    if template_num in templates:
        return PromptTemplate(input_variables=["context", "question"], template=templates[template_num])
    else:
        st.write("Please choose a valid template")

# Function to generate chatbot response
def generate_response(prompt):
    knowledge_base = Chroma(persist_directory="./chroma_db_conversational_chat")
    llm = Ollama(model="mistral", temperature=0.2, callback_manager=StreamingStdOutCallbackHandler())

    qa_chain = RetrievalQA.from_chain_type(llm, chain_type="stuff",
                                           retriever=knowledge_base.as_retriever(search_kwargs={"k": 2}),
                                           chain_type_kwargs={"prompt": build_prompt("template_1")})
    answer = qa_chain({"query": prompt})
    return answer["result"]

# Streamlit app
st.title("RAG Chatbot Streamlit")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat interface
prompt = st.text_input("What's on your mind?")
if prompt:
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.empty():
        # Generate and display bot response
        bot_response = generate_response(prompt)
        st.session_state["messages"].append({"role": "bot", "content": bot_response})
        st.write(bot_response)

# Display chat history
for message in st.session_state["messages"]:
    with st.expander(message["role"]):
        st.write(message["content"])











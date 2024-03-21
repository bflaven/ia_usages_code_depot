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
streamlit run 008_rag_chatbot_with_streamlit.py


"""


import asyncio
import ollama
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter

# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initializing Streamlit app
st.title("Conversational Chat")

models = [model["name"] for model in ollama.list()["models"]]
st.session_state["model"] = st.selectbox("Choose your model", models)

# Checking and initializing session state variables
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "prompt" not in st.session_state:
    st.session_state["prompt"] = ""

# init models
if "model" not in st.session_state:
    st.session_state["model"] = ""

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

    async def stream_qa_chain(_qa_chain, prompt):
        with st.spinner("Generating response..."):
            async for response in qa_chain.agenerate([{"query": prompt}]):
                yield response["result"]

    loop = asyncio.get_event_loop()
    stream = loop.run_until_complete(stream_qa_chain(qa_chain, prompt))
    for chunk in stream:
        yield chunk

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # add latest message to history in format {role, content}
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message = st.write_stream(chat_res_generator(prompt))
        st.session_state["messages"].append({"role": "assistant", "content": message})






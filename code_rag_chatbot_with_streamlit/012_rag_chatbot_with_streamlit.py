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
streamlit run _GOOD_012_rag_chatbot_with_streamlit.py


"""



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

# Import for reading file
import pathlib

# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# import pathlib
# import streamlit as st
# from openai_ollama import Ollama, OllamaEmbeddings, CallbackManager, StreamingStdOutCallbackHandler
# from openai_ollama import RetrievalQA, PromptTemplate
# from lhotse.audio import AudioSource, Recording
# from lhotse.cut import MonoCut
# from lhotse.features import FeatureSetBuilder, Fbank, FbankConfig
# from lhotse.recipes import prepare_librispeech, prepare_musan
# from lhotse.utils import Pathlike

# Function to build prompt
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
        st.write("Please choose a valid template")

# Chat application class
class ChatApp:
    def __init__(self):
        # init models
        if "model" not in st.session_state:
            st.session_state["model"] = ""
            
        # Checking and initializing session state variables
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        if "prompt" not in st.session_state:
            st.session_state["prompt"] = ""

    # Chat response generator
    def chat_res_generator(self, prompt, file_path):
        
        # Mistral Settings
        embeddings_open = OllamaEmbeddings(model="mistral")
        llm_open = Ollama(model="mistral", temperature=0.5, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

        # Read the file
        file_path = pathlib.Path(file_path)
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
        answer = qa_chain({"query": prompt})
        result = answer["result"]

        

        # Getting response from QA chain
        def stream_qa_chain(_qa_chain, prompt):
            with st.spinner("Generating response..."):
                yield result

        stream = stream_qa_chain(qa_chain, prompt)
        for chunk in stream:
            yield chunk

    # Run the chat app
    def run(self):
        models = [model["name"] for model in ollama.list()["models"]]
        st.session_state["model"] = st.selectbox("Choose your model", models)

        # Display chat messages from history on app rerun
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("What is up?"):
            # Add latest message to history in format {role, content}
            st.session_state["messages"].append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                file_path = "../_data/fake_small_bio.txt"
                message = st.write_stream(self.chat_res_generator(prompt, file_path))
                st.session_state["messages"].append({"role": "assistant", "content": message})

# Main function
if __name__ == "__main__":
    chat_app = ChatApp()
    chat_app.run()






# 004_prompt_conversational_chat.md

## prompt
As an advanced programmer in Python using Langchain, Chroma and Streamlit, in the this function replace the "user_input_source" variable by "user_input_source = st.file_uploader("Upload a document", type=["txt", "pdf", "docx", "html", "css", "py", "csv"])"  and make it work.user_input_sourceRewirte the all script.

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


## output_chatgpt
Below is the updated script with the changes you requested:

```python
import os
import tempfile
import pathlib
import csv
import streamlit as st
from pdfminer.high_level import extract_text as extract_text_pdf
import docx
from chroma import Chroma, OllamaEmbeddings, Ollama, CallbackManager, StreamingStdOutCallbackHandler
from chroma.models.templates import PromptTemplate
from rag.retrieval_qa import RetrievalQA
from rag.splitter import CharacterTextSplitter

class ChromaChatApp:
    def __init__(self):
        self.user_input_source = None
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
        if user_input_source is None:
            return ""

        file_extension = os.path.splitext(user_input_source.name)[1][1:]
        text = ""

        if file_extension in ["txt"]:
            try:
                text = user_input_source.getvalue().decode("utf-8")
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
                text = user_input_source.getvalue().decode("utf-8")
            except Exception as e:
                print(f"Error reading {file_extension.upper()} file:", e)

        elif file_extension == "csv":
            try:
                text = user_input_source.getvalue().decode("utf-8")
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
        self.user_input_source = st.file_uploader("Upload a document", type=["txt", "pdf", "docx", "html", "css", "py", "csv"])
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
```

In this updated script:

- I replaced the `st.text_input` for file uploading with `st.file_uploader` in the `run()` method.
- Modified the `file_uploader` method to handle file uploaders from Streamlit correctly.
- Changed the logic in the `file_uploader` method to handle file objects correctly based on their types.
- Adjusted the usage of the `user_input_source` variable throughout the script to reflect the changes.


## output_mistral



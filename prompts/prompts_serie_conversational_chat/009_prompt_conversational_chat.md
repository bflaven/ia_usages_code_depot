# 004_prompt_conversational_chat.md

## prompt
As an advanced programmer in Python using Langchain, Chroma and Streamlit, can you write a Python script, with the best practices (Class, code commented, Functions... etc.) of an app that fulfill several functions.
Each specific function will be separated in streamlit tabs.
- Tab_1 : Create a chroma database named "chroma_db_conversational_chat". Check if the base has been already created, if yes mention it.
- Tab_3 : Enable the ingestion of documents such as .pdf, .docx, .txt that are then store in the newly database named "chroma_db_conversational_chat".
- Tab_2 : Enable the request of this database named "chroma_db_conversational_chat" with a prompt named "template_1".


## output_chatgpt


Below is a Python script that fulfills the requirements you provided using Langchain, Chroma, and Streamlit. The script is structured with classes, functions, and comments for better readability and organization:

```python
import streamlit as st
import os
from chroma import ChromaDB

class ChromaApp:
    def __init__(self):
        self.db_name = "chroma_db_conversational_chat"
        self.db_path = f"./{self.db_name}.db"
        self.db_created = os.path.exists(self.db_path)
        self.db = ChromaDB(self.db_path)

    def create_database_tab(self):
        st.title("Create Chroma Database")
        if self.db_created:
            st.write(f"Database '{self.db_name}' already exists.")
        else:
            self.db.create_database()
            st.write(f"Database '{self.db_name}' created successfully.")

    def ingest_documents_tab(self):
        st.title("Ingest Documents to Database")
        st.write("Upload documents (.pdf, .docx, .txt) to store in the database.")

        uploaded_files = st.file_uploader("Upload Files", type=["pdf", "docx", "txt"], accept_multiple_files=True)

        if uploaded_files:
            for file in uploaded_files:
                content = file.getvalue().decode("utf-8")
                self.db.store_document(content)
                st.write(f"File '{file.name}' ingested successfully.")

    def request_database_tab(self):
        st.title("Request Database")
        st.write("Enter your request template to query the database.")

        template_1 = st.text_input("Enter Template 1")

        if st.button("Submit"):
            results = self.db.query(template_1)
            st.write("Results:")
            st.write(results)

    def run(self):
        st.sidebar.title("Chroma App")
        tab_selection = st.sidebar.radio("Select Tab", ["Create Database", "Ingest Documents", "Request Database"])

        if tab_selection == "Create Database":
            self.create_database_tab()
        elif tab_selection == "Ingest Documents":
            self.ingest_documents_tab()
        elif tab_selection == "Request Database":
            self.request_database_tab()

if __name__ == "__main__":
    app = ChromaApp()
    app.run()
```

This script defines a `ChromaApp` class that encapsulates the functionality of the Streamlit app. The class contains methods for each tab: `create_database_tab`, `ingest_documents_tab`, and `request_database_tab`. The `run` method is the entry point of the Streamlit app, which sets up the UI and handles user interactions.

Please make sure you have installed the required packages (`streamlit` and `chroma`) before running the script. You can install them using pip:

```bash
pip install streamlit chroma
```

You also need to have Langchain, Chroma, and Streamlit configured and installed properly for this script to work as expected. Additionally, ensure that you have appropriate permissions to read and write files in the directory where you run the script.





## output_mistral

Here's a Python script that fulfills the requirements you've specified using Langchain, Chroma, and Streamlit. I've created a class named `ConversationalChatApp` and separated the functions into Streamlit tabs as requested.

```python
import os
import streamlit as st
from langchain.document_loaders import PyPDFLoader, TextLoader, UnstructuredFileLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Set up the Hugging Face embeddings model
embeddings = HuggingFaceEmbeddings()

class ConversationalChatApp:
    def __init__(self):
        self.db_name = "chroma_db_conversational_chat"
        self.template_1 = "Answer the following question based on the context provided: {question}"
        self.qa_chain = RetrievalQA.from_chain_type(llm=None, chain_type="stuff", retriever=None, return_source_documents=True)

    def check_database(self):
        if os.path.exists(self.db_name):
            st.write(f"The database '{self.db_name}' already exists.")
        else:
            st.write(f"The database '{self.db_name}' does not exist.")

    def create_database(self):
        if not os.path.exists(self.db_name):
            st.write(f"Creating the database '{self.db_name}'...")
            self.vectorstore = Chroma(persist_directory=self.db_name, embedding_function=embeddings)
            st.write(f"The database '{self.db_name}' has been successfully created.")
        else:
            st.write(f"The database '{self.db_name}' already exists. Loading the database...")
            self.vectorstore = Chroma(persist_directory=self.db_name, embedding_function=embeddings)

    def ingest_documents(self, files):
        for file in files:
            file_extension = os.path.splitext(file.name)[1]

            if file_extension == ".pdf":
                loader = PyPDFLoader(file)
            elif file_extension in [".docx", ".doc"]:
                loader = UnstructuredFileLoader(file, mode="elements")
            elif file_extension in [".txt"]:
                loader = TextLoader(file)
            else:
                st.write(f"Unsupported file format: {file_extension}")
                continue

            documents = loader.load()
            self.vectorstore.add_documents(documents)
            st.write(f"Ingested {len(documents)} documents from {file.name}.")

    def request_database(self, prompt):
        result = self.qa_chain.run(input_documents=self.vectorstore, question=prompt, chain_type_kwargs={"prompt": self.template_1})
        st.write(result)

def main():
    app = ConversationalChatApp()

    st.title("Conversational Chat App")

    tab1, tab2, tab3 = st.tabs(["Database", "Request", "Ingest Documents"])

    with tab1:
        st.header("Tab 1: Database Management")
        app.check_database()
        if st.button("Create Database"):
            app.create_database()

    with tab3:
        st.header("Tab 3: Ingest Documents")
        files = st.file_uploader("Upload documents", type=["pdf", "docx", "txt"], accept_multiple_files=True)
        if st.button("Ingest Documents") and files:
            app.ingest_documents(files)

    with tab2:
        st.header("Tab 2: Request Database")
        prompt = st.text_input("Enter your prompt:")
        if st.button("Request") and prompt:
            app.request_database(prompt)

if __name__ == "__main__":
    main()
```

This script creates a Streamlit app with three tabs:

1. Tab 1: Database Management - Checks if the database exists and allows you to create it.
2. Tab 3: Ingest Documents - Enables the ingestion of documents (PDF, DOCX, TXT) that are stored in the database.
3. Tab 2: Request Database - Allows you to request the database with a prompt using the template "template_1".

The app uses the `ConversationalChatApp` class to handle the functionality. Make sure you have the required packages installed and run the script using `streamlit run script_name.py`.

# 003_prompt_conversational_chat.md

## prompt
As an advanced programmer in Python using Langchain and Chroma, can you write a different python script that query the existing Chroma database named "chroma_db_conversational_chat" based on the variable "user_input_source" and "user_input_prompt". Manage the case where the "user_input_source" and "user_input_prompt" are empty because the user has not idea on what to query and has no document to send.

Leverage on the code below in terms of coding.

user_input_source = "_data/empty_file.txt"
user_input_prompt= "the prompt by the user"

# Create your own prompt by using the template below.
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
        print("Please choose a valid template")

# Mistral Settings
embeddings_open = OllamaEmbeddings(model="mistral")
llm_open = Ollama(model="mistral", temperature=0.2, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

# Read the file
file_path = pathlib.Path(user_input_source)
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
answer = qa_chain({"query": user_input})
result = answer["result"]

print('\n')

## output

Sure, I can help you modify the script to handle empty inputs and query the existing Chroma database. Here's a revised version of your script:

```python
import os
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler

user_input_source = "_data/empty_file.txt"
user_input_prompt= "the prompt by the user"

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
        print("Please choose a valid template")

# Mistral Settings
embeddings_open = OllamaEmbeddings(model="mistral")
llm_open = Ollama(model="mistral", temperature=0.2, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

# Initialize Chroma
knowledge_base = Chroma(persist_directory="./chroma_db_conversational_chat", embedding_function=embeddings_open)

# Handle empty user input
if os.path.exists(user_input_source) and os.path.getsize(user_input_source) > 0:
    file_path = pathlib.Path(user_input_source)
    text = file_path.read_text()
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    chunks = text_splitter.split_text(text)
else:
    print("No document provided or the document is empty.")
    chunks = []

# Initialize prompt
prompt = build_prompt("template_1")

# Initialize RetrievalQA
if user_input_prompt:
    qa_chain = RetrievalQA.from_chain_type(llm_open, chain_type="stuff", retriever=knowledge_base.as_retriever(), chain_type_kwargs={"prompt": prompt})
    answer = qa_chain({"query": user_input_prompt})
    result = answer["result"]
    print('\n', result)
else:
    print("No query provided by the user.")
```

This script first checks if the provided file exists and is not empty. If it is, it prints a message and sets `chunks` to an empty list. Then, it checks if `user_input_prompt` is not empty. If it is, it prints a message. If it's not, it queries the Chroma database and prints the result.

## input
Rewrite the all script and ask to the user at the beginning to define "user_input_source" and "user_input_prompt"

## output

Sure, here's a revised version of the script that asks the user to define `user_input_source` and `user_input_prompt` at the beginning:

```python
import os
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler

# Ask the user to define user_input_source and user_input_prompt
user_input_source = input("Please enter the path to the source file: ")
user_input_prompt = input("Please enter the prompt for the query: ")

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
        print("Please choose a valid template")

# Mistral Settings
embeddings_open = OllamaEmbeddings(model="mistral")
llm_open = Ollama(model="mistral", temperature=0.2, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

# Handle empty user input
if os.path.exists(user_input_source) and os.path.getsize(user_input_source) > 0:
    file_path = pathlib.Path(user_input_source)
    text = file_path.read_text()
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    chunks = text_splitter.split_text(text)
else:
    print("No document provided or the document is empty.")
    chunks = []

# Initialize Chroma
knowledge_base = Chroma(persist_directory="./chroma_db_conversational_chat", embedding_function=embeddings_open)

# Initialize prompt
prompt = build_prompt("template_1")

# Initialize RetrievalQA
if user_input_prompt:
    qa_chain = RetrievalQA.from_chain_type(llm_open, chain_type="stuff", retriever=knowledge_base.as_retriever(), chain_type_kwargs={"prompt": prompt})
    answer = qa_chain({"query": user_input_prompt})
    result = answer["result"]
    print('\n', result)
else:
    print("No query provided by the user.")
```

This script first asks the user to enter the path to the source file and the prompt for the query. It then checks if the provided file exists and is not empty. If it is, it prints a message and sets `chunks` to an empty list. Then, it initializes the Chroma database and the prompt. Finally, it checks if `user_input_prompt` is not empty. If it is, it prints a message. If it's not, it queries the Chroma database and prints the result.


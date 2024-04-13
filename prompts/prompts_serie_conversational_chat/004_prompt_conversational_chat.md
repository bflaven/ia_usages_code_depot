# 004_prompt_conversational_chat.md

## prompt
As an advanced programmer in Python using Langchain and Chroma, can you extend this python script to enable the ingest of .pdf files and manage the case where the "user_input" is empty because the user has not idea on what to query and also as document to send in PATH_TO_SOURCE.
Leverage on the previous code in terms of coding.

```python
user_input = input("Enter your question: ")
if not user_input:
    print("Please enter a valid question.")
    exit()

# without CV, does not know
PATH_TO_SOURCE = "_data/cv_resume_bruno_flaven_2023_1.pdf"
user_input= "What is HECUBE?"
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
file_path = pathlib.Path(PATH_TO_SOURCE)
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

# print('\n –-- RESULT')
# print(result)


# "Mal nommer les choses, c'est ajouter au malheur du monde !" Albert Camus

```


## output

Sure, I can help you extend your script to handle PDF files and manage cases where the user input is empty. Here's how you can modify your script:

```python
import textract
import os
import pathlib
from langchain import Ollama, OllamaEmbeddings, RetrievalQA, PromptTemplate, CharacterTextSplitter, Chroma
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pathlib

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file"""
    text = textract.process(file_path).decode("utf-8")
    return text

def build_prompt(template_num="template_1"):
    # Your existing build_prompt function here
    pass

def handle_empty_query():
    """Generate a prompt for when the user doesn't provide a query"""
    return "Can you provide a summary of the document?"

# Mistral Settings
embeddings_open = OllamaEmbeddings(model="mistral")
llm_open = Ollama(model="mistral", temperature=0.2, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

# Path to the source PDF file
PATH_TO_SOURCE = "_data/cv_resume_bruno_flaven_2023_1.pdf"

# Extract text from the PDF file
text = extract_text_from_pdf(PATH_TO_SOURCE)

# Initialize text splitter
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = text_splitter.split_text(text)

# Initialize Chroma
knowledge_base = Chroma.from_texts(chunks, embeddings_open, persist_directory="./chroma_db_conversational_chat")

# Initialize prompt
prompt = build_prompt("template_1")

# Initialize RetrievalQA
qa_chain = RetrievalQA.from_chain_type(llm_open, chain_type="stuff", retriever=knowledge_base.as_retriever(), chain_type_kwargs={"prompt": prompt})

# Get user input
user_input = input("Enter your question: ")
if not user_input:
    user_input = handle_empty_query()

# Get answer
answer = qa_chain({"query": user_input})
result = answer["result"]

print('\n')
print(result)
```

This script uses the `textract` library to extract text from PDF files. If the user doesn't provide a query, it generates a default query asking for a summary of the document. Please ensure that you have the `textract` library installed in your Python environment. If not, you can install it using pip:

```bash
pip install textract
```

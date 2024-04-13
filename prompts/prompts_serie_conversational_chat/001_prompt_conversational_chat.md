# 001_prompt_conversational_chat.md

## prompt
As an advanced programmer in Python using Langchain and Chroma, can you write a python script that extract the text from a text file named "sample_transcript.txt" then it will use the "text_splitter" to load into a Chroma database named "chroma_db_conversational_chat"

You can use the code below and please write the full script from import to the treament.

# LangChain Imports
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


# Text treatment
user_input= "That will be question made by the user"

template_1 = """You are a helpful chatbot, created by the RSLT Team. You answer the questions of the customers giving a lot of details based on what you find in the context.
    You are to act as though you're having a conversation with a human.
    You are only able to answer questions, guide and assist, and provide recommendations to users. You cannot perform any other tasks outside of this.
    Your tone should be professional and friendly.
    Your purpose is to answer questions people might have, however if the question is unethical you can choose not to answer it.
    Your responses should always be one paragraph long or less.
    Context: {context}
    Question: {question}
    Helpful Answer:"""

text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = text_splitter.split_text(text)
knowledge_base = Chroma.from_texts(chunks, embeddings_open, persist_directory="./chroma_db_conversational_chat")

text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
                chunks = text_splitter.split_text(text)

knowledge_base = Chroma.from_texts(chunks, embeddings_open, persist_directory="./chroma_db")
docs = knowledge_base.similarity_search(user_input)

llm = Ollama(model="mistral", temperature=0, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

prompt = PromptTemplate(input_variables=["context", "question"], template=template_1)

qa_chain = RetrievalQA.from_chain_type(llm_open, chain_type="stuff", retriever=knowledge_base.as_retriever(), chain_type_kwargs={"prompt": build_prompt("template_1")})
answer = qa_chain({"query": user_input})
result = answer["result"]


## output
Sure, I can help you write a Python script that uses Langchain and Chroma to extract text from a file and load it into a Chroma database. Here's a script based on the code you provided:

```python
# LangChain Imports
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts.prompt import PromptTemplate

# Import for reading file
import pathlib

# Text treatment
user_input= "That will be question made by the user"

template_1 = """You are a helpful chatbot, created by the RSLT Team. You answer the questions of the customers giving a lot of details based on what you find in the context.
    You are to act as though you're having a conversation with a human.
    You are only able to answer questions, guide and assist, and provide recommendations to users. You cannot perform any other tasks outside of this.
    Your tone should be professional and friendly.
    Your purpose is to answer questions people might have, however if the question is unethical you can choose not to answer it.
    Your responses should always be one paragraph long or less.
    Context: {context}
    Question: {question}
    Helpful Answer:"""

# Read the file
file_path = pathlib.Path("sample_transcript.txt")
text = file_path.read_text()

# Initialize text splitter
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = text_splitter.split_text(text)

# Initialize Chroma
knowledge_base = Chroma.from_texts(chunks, embeddings_open, persist_directory="./chroma_db_conversational_chat")

# Initialize Ollama
llm = Ollama(model="mistral", temperature=0, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

# Initialize prompt
prompt = PromptTemplate(input_variables=["context", "question"], template=template_1)

# Initialize RetrievalQA
qa_chain = RetrievalQA.from_chain_type(llm_open, chain_type="stuff", retriever=knowledge_base.as_retriever(), chain_type_kwargs={"prompt": build_prompt("template_1")})

# Get answer
answer = qa_chain({"query": user_input})
result = answer["result"]
```

Please note that you need to replace `embeddings_open` and `llm_open` with your actual embeddings and language model objects. Also, make sure that the file "sample_transcript.txt" is in the same directory as your script, or provide the full path to the file.

This script assumes that you have the necessary permissions to read the file and write to the directory specified for the Chroma database. If you encounter any issues, please check your permissions and the correctness of your file paths.


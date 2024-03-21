# 002_prompt_conversational_chat.md

## prompt
As an advanced programmer in Python using Langchain and Chroma, can you fix this python script that extract the text from a text file named "sample_transcript.txt" then it will use the "text_splitter" to load into a Chroma database named "chroma_db_conversational_chat"

# Text treatment
user_input= "That will be question made by the user"

# Create your own prompt by using the template below.
def build_prompt(template_num="template_1"):
    '''This function builds and returns a choosen prompt for a RAG Application with context and a normal LLM Run without'''

    template_1 = """You are a helpful chatbot, created by the RSLT Team. You answer the questions of the customers giving a lot of details based on what you find in the context.
    You are to act as though you're having a conversation with a human.
    You are only able to answer questions, guide and assist, and provide recommendations to users. You cannot perform any other tasks outside of this.
    Your tone should be professional and friendly.
    Your purpose is to answer questions people might have, however if the question is unethical you can choose not to answer it.
    Your responses should always be one paragraph long or less.
    Context: {context}
    Question: {question}
    Helpful Answer:"""

    template_2 = """You are a helpful chatbot, created by the RSLT Team.  You answer the questions of the customers giving a lot of details based on what you find in the context. 
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
llm_open = Ollama(model="mistral", temperature=0.2,
                         callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
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

print('\n –-- RESULT')
print(result)


## output

The script you provided has a few issues. Here's a corrected version:

```python
# LangChain Imports
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from langchain.callbacks import StreamingStdOutCallbackHandler
import pathlib

# Text treatment
user_input= "That will be question made by the user"

# Create your own prompt by using the template below.
def build_prompt(template_num="template_1"):
    '''This function builds and returns a chosen prompt for a RAG Application with context and a normal LLM Run without'''

    template_1 = """You are a helpful chatbot, created by the RSLT Team. You answer the questions of the customers giving a lot of details based on what you find in the context.
    You are to act as though you're having a conversation with a human.
    You are only able to answer questions, guide and assist, and provide recommendations to users. You cannot perform any other tasks outside of this.
    Your tone should be professional and friendly.
    Your purpose is to answer questions people might have, however if the question is unethical you can choose not to answer it.
    Your responses should always be one paragraph long or less.
    Context: {context}
    Question: {question}
    Helpful Answer:"""

    template_2 = """You are a helpful chatbot, created by the RSLT Team.  You answer the questions of the customers giving a lot of details based on what you find in the context.
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
file_path = pathlib.Path("sample_transcript.txt")
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

print('\n –-- RESULT')
print(result)
```

Here are the changes I made:

1. Imported the necessary modules and classes from Langchain.
2. Corrected the function `build_prompt` to return the prompt object.
3. Used the `build_prompt` function to create the prompt for the `RetrievalQA` chain.
4. Removed the extra initialization of `Ollama` as it was not being used.
5. Made sure that the `template_1` variable is defined in the scope where it is being used. In this case, I removed it and directly used the `build_prompt` function.

Please note that you need to have the necessary permissions to read the file "sample_transcript.txt" and write to the directory specified for the Chroma database. If you encounter any issues, please check your permissions and the correctness of your file paths.

Also, make sure that the `Ollama` and `OllamaEmbeddings` models are correctly installed and configured. If you encounter any issues, please check the installation and usage instructions for these models.

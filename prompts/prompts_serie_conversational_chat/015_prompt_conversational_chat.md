# 004_prompt_conversational_chat.md

## prompt
As an advanced programmer in Python using Langchain, Chroma and Streamlit, can you rewrite the Python code below and fix it so the "qa_chain" can be retrieved in a stream e.g stream = ollama.chat(
        model=st.session_state["model"],
        messages=st.session_state["messages"],
        stream=True,
    )

```python
# Importing necessary libraries
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
st.title("Conversational Chat with Chroma DB")

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
def chat_res_generator():

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
    
    # Getting response from QA chain
    # message = qa_chain({"query": prompt})
    # message = answer["result"]
    # return message

    stream = ollama.chat(
        model=st.session_state["model"],
        messages=st.session_state["messages"],
        stream=True,
    )
    for chunk in stream:
        yield chunk["message"]["content"]



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
        message = st.write_stream(chat_res_generator())
        st.session_state["messages"].append({"role": "assistant", "content": message})
```





## output_mistral

Sure, I can help you modify your code to retrieve the "qa_chain" in a stream. Here's how you can do it:

```python
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
st.title("Conversational Chat with Chroma DB")

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

    # Getting response from QA chain
    @streamlit.cache_resource
    def stream_qa_chain(qa_chain, prompt):
        with st.spinner("Generating response..."):
            response = qa_chain({"query": prompt})
            yield response["result"]

    stream = stream_qa_chain(qa_chain, prompt)
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
```

In this code, I've added a new function `stream_qa_chain` that generates the response from the QA chain in a stream. This function is then called in `chat_res_generator` to yield the response in chunks.


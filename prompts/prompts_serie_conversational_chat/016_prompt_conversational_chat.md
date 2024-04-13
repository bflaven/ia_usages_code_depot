# 004_prompt_conversational_chat.md

## prompt
/opt/homebrew/lib/python3.11/site-packages/streamlit/util.py:227: RuntimeWarning: coroutine 'expire_cache' was never awaited
  pass



## output_mistral

The warning message you're seeing, "coroutine 'expire\_cache' was never awaited", is related to the use of the `@streamlit.cache_resource` decorator in the previous code snippet. This decorator is intended to be used with synchronous functions, but the `stream_qa_chain` function is a coroutine, which is causing the warning.

To resolve this warning, you can remove the `@streamlit.cache_resource` decorator from the `stream_qa_chain` function. However, this will also remove the caching of the function's output, which could impact performance if the function is called frequently with the same inputs.

Here's the updated code without the decorator:

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
    async def stream_qa_chain(qa_chain, prompt):
        with st.spinner("Generating response..."):
            response = await qa_chain.agenerate([{"query": prompt}])
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

In this updated code, I've also modified the `stream_qa_chain` function to use the `agenerate` method of the `qa_chain` object, which is an asynchronous generator that can be used to stream the response.


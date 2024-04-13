# prompt_api_24.md

## prompt
As an advanced programmer in Python, with FastAPI, create an endpoint named "/seo/titles". The variable "content" is the one that will post inside this endpoint. The code is the one below and make also an error management.



```python
import warnings
import os 
import json



# For LLM
import langchain
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import SimpleSequentialChain
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser #PydanticOutputParser
# from langchain_core.pydantic_v1 import BaseModel, Field, validator

# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)



'''
Run mistral and get outputs for this large language model
'''


'''loading the model'''

# SimpleSequentialChain
llm_model="mistral:latest"


SYSTEM_PROMPT = "You are a smart and intelligent journalist, craft three compelling titles for an online post about the topic given in the content, ensuring to incorporate SEO best practices with the most common keywords from the content. Here is the format for each proposal inside an object with title as dictionary. Content: {content}""\nOutput:"

llm = Ollama(temperature=0.9, model=llm_model)

# prompt template 1
first_prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

# Chain 1
chain_one = LLMChain(llm=llm, prompt=first_prompt)
overall_simple_chain = SimpleSequentialChain(chains=[chain_one], verbose=False)

result = overall_simple_chain.invoke(content)
```


## output
To create a FastAPI endpoint named "/seo/titles" that accepts a POST request with JSON data containing a "content" field, and handles error management, you can use the following code:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import your libraries and dependencies here
import warnings
import os 
import json

# For LLM
import langchain
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import SimpleSequentialChain
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser 

# disable for the moment deprecated message
warnings.filterwarnings("ignore", category=UserWarning)

# Define your FastAPI app
app = FastAPI()

# Define a Pydantic model to validate incoming JSON data
class ContentRequest(BaseModel):
    content: str

# Define your LLM setup
llm_model = "mistral:latest"
SYSTEM_PROMPT = "You are a smart and intelligent journalist, craft three compelling titles for an online post about the topic given in the content, ensuring to incorporate SEO best practices with the most common keywords from the content. Here is the format for each proposal inside an object with title as dictionary. Content: {content}""\nOutput:"
llm = Ollama(temperature=0.9, model=llm_model)
first_prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
chain_one = LLMChain(llm=llm, prompt=first_prompt)
overall_simple_chain = SimpleSequentialChain(chains=[chain_one], verbose=False)

# Define your endpoint
@app.post("/seo/titles")
async def generate_titles(content_request: ContentRequest):
    try:
        # Process the content and generate titles
        content = content_request.content
        result = overall_simple_chain.invoke(content)
        
        # Return the result
        return {"titles": result}
    except Exception as e:
        # Handle any errors and return an appropriate HTTPException
        raise HTTPException(status_code=500, detail="Internal Server Error")
```

This code sets up a FastAPI application with an endpoint at "/seo/titles" that expects a POST request with JSON data containing a "content" field. It then processes the content using the provided LLM setup and returns the generated titles in the response. If any errors occur during processing, it returns a 500 Internal Server Error with an appropriate message.


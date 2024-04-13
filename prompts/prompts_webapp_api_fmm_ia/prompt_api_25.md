# prompt_api_24.md

## prompt
Create an end-point named "/seo/titles" where a variable "text_for_title" is sent to an LMM defined in llm_model and with SYSTEM_PROMPT where {content} is replaced by the value sent in the variable "text_for_title". For the readability of the code,   externalize the LMM stuff inside a file external name "llm_mistral.py" then wait for the result of the prompt and send it back to a fastAPI end-point as a dictionary.

```python
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

To achieve your requirements, you'll need to organize your code into several components: the FastAPI endpoint, the function that interacts with the LLM model, and an external file to handle LLM-related functionalities. Let's structure the code accordingly.

First, create a file named `llm_mistral.py` and add the necessary LLM-related functionalities:

```python
# llm_mistral.py

import langchain
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import SimpleSequentialChain

class LLMManager:
    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.llm = Ollama(temperature=0.9, model=self.llm_model)

    def generate_titles(self, content):
        SYSTEM_PROMPT = "You are a smart and intelligent journalist, craft three compelling titles for an online post about the topic given in the content, ensuring to incorporate SEO best practices with the most common keywords from the content. Here is the format for each proposal inside an object with title as dictionary. Content: {content}\nOutput:"
        prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
        chain = LLMChain(llm=self.llm, prompt=prompt)
        overall_chain = SimpleSequentialChain(chains=[chain], verbose=False)
        return overall_chain.invoke(content)
```

Next, integrate this functionality into your FastAPI endpoint:

```python
# main.py

from fastapi import FastAPI
from llm_mistral import LLMManager

app = FastAPI()

llm_manager = LLMManager(llm_model="mistral:latest")

@app.post("/seo/titles")
async def generate_titles(text_for_title: str):
    titles = llm_manager.generate_titles(text_for_title)
    return {"titles": titles}
```

Ensure that both files are in the same directory. Now, when you send a POST request to `/seo/titles` with `text_for_title` as the request body, it will generate titles using the LLM model and return them as a dictionary.

Make sure you have all dependencies installed, including `fastapi` and `uvicorn`. You can install them via pip if you haven't already:

```bash
pip install fastapi uvicorn
```

Then, you can run your FastAPI server using the following command:

```bash
uvicorn main:app --reload
```

This command assumes that your FastAPI application is defined in a file named `main.py`. Adjust the file name accordingly if it's different.

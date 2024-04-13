# prompt_api_34.md

## prompt_1

As an advanced programmer in Python, with FastAPI, for the code below, simplify and apply all best practices such as DRY to this chunk of code:
- Create a class
- Load it from an external file
- Make a single endpoint from this code
- Externalise the values SEO_ENGLISH_SYSTEM_PROMPT, SEO_FRENCH_SYSTEM_PROMPT, SMO_ENGLISH_SYSTEM_PROMPT and make a variable that should call by a single function.

```python
#########################  Endpoints for Social (packaging) #################################

class OllamaRequest(BaseModel):
    # model: str
    content: str
    # stream: bool

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_REQUEST_MODEL = "mistral:latest"
OLLAMA_REQUEST_STREAM = False


# SEO FOR ENGLISH
SEO_ENGLISH_SYSTEM_PROMPT = (
    "You are a smart and intelligent journalist. Craft three compelling titles for an online post about the topic given in the content, ensuring to incorporate SEO best practices with the most common keywords from the content. For each proposal, print only the result in a Python dictionary object with title as a string and keywords as a list and include the all result into a Python list object like define below."
    "\n"
    "Output Format:\n"
    "["
    "{{\"title\": \"The value of the title\", \"keywords\": [list of keywords]}},"
    "{{\"title\": \"The value of the title\", \"keywords\": [list of keywords]}},"
    "{{\"title\": \"The value of the title\", \"keywords\": [list of keywords]}}"
    "]"
    "\n"
    "Content: {content}"
    # " Content: {content}".format(content="{content}")
)

# SEO FOR FRENCH
SEO_FRENCH_SYSTEM_PROMPT = (
    "You are a French smart and intelligent journalist. Craft three compelling titles in French for an online post about the topic given in the content in French, ensuring to incorporate SEO best practices with the most common keywords from the content. For each proposal, print in French only the result in a Python dictionary object with title as a string and keywords as a list and include the all result into a Python list object like define below."
    "\n"
    "Output Format:\n"
    "["
    "{{\"title\": \"The value of the title\", \"keywords\": [list of keywords]}},"
    "{{\"title\": \"The value of the title\", \"keywords\": [list of keywords]}},"
    "{{\"title\": \"The value of the title\", \"keywords\": [list of keywords]}}"
    "]"
    "\n"
    "Content: {content}"
    # " Content: {content}".format(content="{content}")
)

# SOCIAL
SMO_ENGLISH_SYSTEM_PROMPT = (
    "You are a smart and intelligent community manager. Craft three compelling messages of 140 caracters each for an online post about the topic given in the content, ensuring to incorporate Social Media Optimization (SMO) best practices with the most common keywords from the content. For each proposal, print only the result in a Python dictionary object with title as a string and hashtags as a list of hashtags and include the all result into a Python list object like define below."
    "\n"
    "Output Format:\n"
    "["
    "{{\"message\": \"The value of the title\", \"hashtags\": [list of hashtags]}},"
    "{{\"message\": \"The value of the title\", \"hashtags\": [list of hashtags]}},"
    "{{\"message\": \"The value of the title\", \"hashtags\": [list of hashtags]}}"
    "]"
    "\n"
    "Content: {content}"
)



@app.post("/llm/seo_english_generate", tags=['seo_english_generate'])
async def seo_english_generate(request: OllamaRequest):
    try:
        prompt_with_content = SEO_ENGLISH_SYSTEM_PROMPT.format(content=request.content)
        data = {
            # "model": request.model,
            "model": OLLAMA_REQUEST_MODEL,
            "prompt": prompt_with_content,
            # "stream": request.stream
            "stream": OLLAMA_REQUEST_STREAM
        }
        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/llm/seo_french_generate", tags=['seo_french_generate'])
async def seo_french_generate(request: OllamaRequest):
    try:
        prompt_with_content = SEO_FRENCH_SYSTEM_PROMPT.format(content=request.content)
        data = {
            # "model": request.model,
            "model": OLLAMA_REQUEST_MODEL,
            "prompt": prompt_with_content,
            # "stream": request.stream
            "stream": OLLAMA_REQUEST_STREAM
        }
        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/llm/smo_generate", tags=['smo_english_generate'])
async def smo_english_generate(request: OllamaRequest):
    try:
        prompt_with_content = SMO_ENGLISH_SYSTEM_PROMPT.format(content=request.content)
        data = {
            # "model": request.model,
            "model": OLLAMA_REQUEST_MODEL,
            "prompt": prompt_with_content,
            # "stream": request.stream
            "stream": OLLAMA_REQUEST_STREAM
        }
        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```


## output_1

Here's a simplified and refactored version of your code applying best practices such as DRY (Don't Repeat Yourself):

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

class OllamaRequest(BaseModel):
    content: str

class OllamaHandler:
    def __init__(self, prompt):
        self.prompt = prompt

    def generate(self, request):
        try:
            prompt_with_content = self.prompt.format(content=request.content)
            data = {
                "model": OllamaHandler.OLLAMA_REQUEST_MODEL,
                "prompt": prompt_with_content,
                "stream": OllamaHandler.OLLAMA_REQUEST_STREAM
            }
            response = requests.post(OllamaHandler.OLLAMA_API_URL, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    OLLAMA_API_URL = "http://localhost:11434/api/generate"
    OLLAMA_REQUEST_MODEL = "mistral:latest"
    OLLAMA_REQUEST_STREAM = False

app = FastAPI()
english_handler = OllamaHandler("""
    You are a smart and intelligent journalist. Craft three compelling titles for an online post about the topic given in the content, ensuring to incorporate SEO best practices with the most common keywords from the content. For each proposal, print only the result in a Python dictionary object with title as a string and keywords as a list and include the all result into a Python list object like define below.
    \n
    Output Format:\n
    [
    {{"title": "The value of the title", "keywords": [list of keywords]}},
    {{"title": "The value of the title", "keywords": [list of keywords]}},
    {{"title": "The value of the title", "keywords": [list of keywords]}}
    ]
    \n
    Content: {content}
""")

french_handler = OllamaHandler("""
    You are a French smart and intelligent journalist. Craft three compelling titles in French for an online post about the topic given in the content in French, ensuring to incorporate SEO best practices with the most common keywords from the content. For each proposal, print in French only the result in a Python dictionary object with title as a string and keywords as a list and include the all result into a Python list object like define below.
    \n
    Output Format:\n
    [
    {{"title": "The value of the title", "keywords": [list of keywords]}},
    {{"title": "The value of the title", "keywords": [list of keywords]}},
    {{"title": "The value of the title", "keywords": [list of keywords]}}
    ]
    \n
    Content: {content}
""")

smo_handler = OllamaHandler("""
    You are a smart and intelligent community manager. Craft three compelling messages of 140 caracters each for an online post about the topic given in the content, ensuring to incorporate Social Media Optimization (SMO) best practices with the most common keywords from the content. For each proposal, print only the result in a Python dictionary object with title as a string and hashtags as a list of hashtags and include the all result into a Python list object like define below.
    \n
    Output Format:\n
    [
    {{"message": "The value of the title", "hashtags": [list of hashtags]}},
    {{"message": "The value of the title", "hashtags": [list of hashtags]}},
    {{"message": "The value of the title", "hashtags": [list of hashtags]}}
    ]
    \n
    Content: {content}
""")

@app.post("/llm/seo_english_generate", tags=['seo_english_generate'])
async def seo_english_generate(request: OllamaRequest):
    return english_handler.generate(request)

@app.post("/llm/seo_french_generate", tags=['seo_french_generate'])
async def seo_french_generate(request: OllamaRequest):
    return french_handler.generate(request)

@app.post("/llm/smo_generate", tags=['smo_english_generate'])
async def smo_english_generate(request: OllamaRequest):
    return smo_handler.generate(request)
```

In this version:
- I created a class `OllamaHandler` to handle the API requests, passing in the appropriate prompt for each type of request.
- I instantiated separate `OllamaHandler` objects for English SEO, French SEO, and SMO, each with their specific prompts.
- I refactored the endpoint functions to use the `OllamaHandler` objects to generate the responses.
- I removed duplicate code by centralizing the common variables and logic inside the `OllamaHandler` class.


# prompt_2
Make a single function from these three endpoints: seo_english_generate, seo_french_generate, smo_generate



# output_2

To consolidate the functionality of the three endpoints (`seo_english_generate`, `seo_french_generate`, `smo_generate`) into a single function, you can use a generic endpoint that takes an additional parameter indicating the type of generation required. Here's how you can do it:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

class OllamaRequest(BaseModel):
    content: str

class OllamaHandler:
    def __init__(self, prompt):
        self.prompt = prompt

    def generate(self, request):
        try:
            prompt_with_content = self.prompt.format(content=request.content)
            data = {
                "model": OllamaHandler.OLLAMA_REQUEST_MODEL,
                "prompt": prompt_with_content,
                "stream": OllamaHandler.OLLAMA_REQUEST_STREAM
            }
            response = requests.post(OllamaHandler.OLLAMA_API_URL, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    OLLAMA_API_URL = "http://localhost:11434/api/generate"
    OLLAMA_REQUEST_MODEL = "mistral:latest"
    OLLAMA_REQUEST_STREAM = False

app = FastAPI()
english_prompt = """
    You are a smart and intelligent journalist. Craft three compelling titles for an online post about the topic given in the content, ensuring to incorporate SEO best practices with the most common keywords from the content. For each proposal, print only the result in a Python dictionary object with title as a string and keywords as a list and include the all result into a Python list object like define below.
    \n
    Output Format:\n
    [
    {{"title": "The value of the title", "keywords": [list of keywords]}},
    {{"title": "The value of the title", "keywords": [list of keywords]}},
    {{"title": "The value of the title", "keywords": [list of keywords]}}
    ]
    \n
    Content: {content}
"""

french_prompt = """
    You are a French smart and intelligent journalist. Craft three compelling titles in French for an online post about the topic given in the content in French, ensuring to incorporate SEO best practices with the most common keywords from the content. For each proposal, print in French only the result in a Python dictionary object with title as a string and keywords as a list and include the all result into a Python list object like define below.
    \n
    Output Format:\n
    [
    {{"title": "The value of the title", "keywords": [list of keywords]}},
    {{"title": "The value of the title", "keywords": [list of keywords]}},
    {{"title": "The value of the title", "keywords": [list of keywords]}}
    ]
    \n
    Content: {content}
"""

smo_prompt = """
    You are a smart and intelligent community manager. Craft three compelling messages of 140 caracters each for an online post about the topic given in the content, ensuring to incorporate Social Media Optimization (SMO) best practices with the most common keywords from the content. For each proposal, print only the result in a Python dictionary object with title as a string and hashtags as a list of hashtags and include the all result into a Python list object like define below.
    \n
    Output Format:\n
    [
    {{"message": "The value of the title", "hashtags": [list of hashtags]}},
    {{"message": "The value of the title", "hashtags": [list of hashtags]}},
    {{"message": "The value of the title", "hashtags": [list of hashtags]}}
    ]
    \n
    Content: {content}
"""

handler_map = {
    "seo_english": OllamaHandler(english_prompt),
    "seo_french": OllamaHandler(french_prompt),
    "smo": OllamaHandler(smo_prompt)
}

@app.post("/llm/generate", tags=['generate'])
async def generate(request: OllamaRequest, type: str):
    if type not in handler_map:
        raise HTTPException(status_code=400, detail="Invalid generation type")
    return handler_map[type].generate(request)
```

In this version:
- I created a single endpoint `/llm/generate` that takes a `type` parameter indicating the type of generation required (`seo_english`, `seo_french`, or `smo`).
- I mapped each type to its corresponding `OllamaHandler` object, initialized with the appropriate prompt.
- The endpoint calls the `generate` method of the appropriate `OllamaHandler` based on the provided type parameter.
- If an invalid type is provided, it returns a 400 Bad Request HTTP response.


# prompt_3

Externalize  OllamaRequest, OllamaHandler in new file to shrink the code. You can give a name meaningfull to this file.

# output_3
To externalize the `OllamaRequest` and `OllamaHandler` classes into a separate file, let's create a module named `ollama.py`. This module will contain the definitions of these classes.

Here's the structure of the module `ollama.py`:

```python
# ollama.py

from pydantic import BaseModel
import requests

class OllamaRequest(BaseModel):
    content: str

class OllamaHandler:
    def __init__(self, prompt):
        self.prompt = prompt

    def generate(self, request):
        try:
            prompt_with_content = self.prompt.format(content=request.content)
            data = {
                "model": OllamaHandler.OLLAMA_REQUEST_MODEL,
                "prompt": prompt_with_content,
                "stream": OllamaHandler.OLLAMA_REQUEST_STREAM
            }
            response = requests.post(OllamaHandler.OLLAMA_API_URL, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    OLLAMA_API_URL = "http://localhost:11434/api/generate"
    OLLAMA_REQUEST_MODEL = "mistral:latest"
    OLLAMA_REQUEST_STREAM = False
```

And here's how you can modify the main file to import these classes from the `ollama` module:

```python
from fastapi import FastAPI, HTTPException
from ollama import OllamaRequest, OllamaHandler

app = FastAPI()
english_prompt = """
    You are a smart and intelligent journalist. Craft three compelling titles for an online post about the topic given in the content, ensuring to incorporate SEO best practices with the most common keywords from the content. For each proposal, print only the result in a Python dictionary object with title as a string and keywords as a list and include the all result into a Python list object like define below.
    \n
    Output Format:\n
    [
    {{"title": "The value of the title", "keywords": [list of keywords]}},
    {{"title": "The value of the title", "keywords": [list of keywords]}},
    {{"title": "The value of the title", "keywords": [list of keywords]}}
    ]
    \n
    Content: {content}
"""

french_prompt = """
    You are a French smart and intelligent journalist. Craft three compelling titles in French for an online post about the topic given in the content in French, ensuring to incorporate SEO best practices with the most common keywords from the content. For each proposal, print in French only the result in a Python dictionary object with title as a string and keywords as a list and include the all result into a Python list object like define below.
    \n
    Output Format:\n
    [
    {{"title": "The value of the title", "keywords": [list of keywords]}},
    {{"title": "The value of the title", "keywords": [list of keywords]}},
    {{"title": "The value of the title", "keywords": [list of keywords]}}
    ]
    \n
    Content: {content}
"""

smo_prompt = """
    You are a smart and intelligent community manager. Craft three compelling messages of 140 caracters each for an online post about the topic given in the content, ensuring to incorporate Social Media Optimization (SMO) best practices with the most common keywords from the content. For each proposal, print only the result in a Python dictionary object with title as a string and hashtags as a list of hashtags and include the all result into a Python list object like define below.
    \n
    Output Format:\n
    [
    {{"message": "The value of the title", "hashtags": [list of hashtags]}},
    {{"message": "The value of the title", "hashtags": [list of hashtags]}},
    {{"message": "The value of the title", "hashtags": [list of hashtags]}}
    ]
    \n
    Content: {content}
"""

handler_map = {
    "seo_english": OllamaHandler(english_prompt),
    "seo_french": OllamaHandler(french_prompt),
    "smo": OllamaHandler(smo_prompt)
}

@app.post("/llm/generate", tags=['generate'])
async def generate(request: OllamaRequest, type: str):
    if type not in handler_map:
        raise HTTPException(status_code=400, detail="Invalid generation type")
    return handler_map[type].generate(request)
```

This way, the code for `OllamaRequest` and `OllamaHandler` is neatly organized into a separate file named `ollama.py`, keeping the main file cleaner and more readable.

# prompt_3

Externalize also english_prompt, french_prompt in new file to shrink the code. You can give a name meaningfull to this file.





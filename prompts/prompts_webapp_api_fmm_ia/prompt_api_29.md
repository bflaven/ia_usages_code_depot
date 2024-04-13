# prompt_api_29.md

## prompt
As an advanced programmer in Python, with FastAPI and Ollama, can you rewrite the code and keep the logic of querying a localhost specified in OLLAMA_API_URL but add a more sophisticated prompt like the one defined in SYSTEM_PROMPT e.g SYSTEM_PROMPT = "You are a smart and intelligent journalist, craft three compelling titles for an online post about the topic given in the content, ensuring to incorporate SEO best practices with the most common keywords from the content. Here is the format for each proposal inside an object with title as dictionary. Content: {content}""\nOutput:".

In SYSTEM_PROMPT, the "{content}" is also a value that is send via the API to Ollama, so the model will return is answer.





from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class OllamaRequest(BaseModel):
    model: str
    prompt: str
    stream: bool

OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.post("/ollama-generate")
async def ollama_generate(request: OllamaRequest):
    try:
        data = {
            "model": request.model,
            "prompt": request.prompt,
            "stream": request.stream
        }
        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




## output
Here's the rewritten code with the sophisticated prompt added:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class OllamaRequest(BaseModel):
    model: str
    content: str
    stream: bool

OLLAMA_API_URL = "http://localhost:11434/api/generate"
SYSTEM_PROMPT = "You are a smart and intelligent journalist, craft three compelling titles for an online post about the topic given in the content, ensuring to incorporate SEO best practices with the most common keywords from the content. Here is the format for each proposal inside an object with title as dictionary. Content: {content}".format(content="{content}")

@app.post("/ollama-generate")
async def ollama_generate(request: OllamaRequest):
    try:
        prompt_with_content = SYSTEM_PROMPT.format(content=request.content)
        data = {
            "model": request.model,
            "prompt": prompt_with_content,
            "stream": request.stream
        }
        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

In this modified version, I've made the following changes:

1. Added a new field `content` to the `OllamaRequest` model to accept the content that will be used in the prompt.
2. Created a `SYSTEM_PROMPT` string that incorporates the content placeholder `{content}`.
3. In the `ollama_generate` function, I'm formatting the `SYSTEM_PROMPT` with the provided content.
4. The formatted prompt is then sent to the OLLAMA API along with other necessary data.

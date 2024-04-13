# prompt_api_26.md

## prompt
As an advanced programmer in Python, with FastAPI and Ollama, can you write the code to integrate the Ollama call below into an endpoint named "ollama-generate" :


curl http://localhost:11434/api/generate -d '{
  "model": "mistral:latest",
  "prompt": "Where is the city Paris?",
  "stream": false
}'




## output


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ollama import Ollama, LLMChain, ChatPromptTemplate, SimpleSequentialChain

app = FastAPI()

# Define the Ollama model and template
llm_model = "mistral:latest"
SYSTEM_PROMPT = "You are a smart and intelligent journalist, craft three compelling titles for an online post about the topic given in the content, ensuring to incorporate SEO best practices with the most common keywords from the content. Here is the format for each proposal inside an object with title as dictionary. Content: {content}""\nOutput:"


llm = Ollama(temperature=0.9, model=llm_model)
first_prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
chain_one = LLMChain(llm=llm, prompt=first_prompt)
overall_simple_chain = SimpleSequentialChain(chains=[chain_one], verbose=False)

class ContentRequest(BaseModel):
    content: str

@app.post("/generate-titles/")
async def generate_titles(request: ContentRequest):
    try:
        result = overall_simple_chain.invoke(request.content)
        return {"titles": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

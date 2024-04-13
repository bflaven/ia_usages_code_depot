# prompt_api_20.md

## prompt
As an advanced programmer in Python, with FastAPI, create an process_text function with this model where example_request is a json model in an external file
async def process_text(body: RecordsRequest = Body(..., example=example_request)):

## output




Here's an example of how you can define a FastAPI endpoint with a `process_text` function that takes a JSON request model from an external file:

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List

# Assume RecordsRequest is defined in an external file
from external_models import RecordsRequest

# Create a FastAPI instance
app = FastAPI()

# Define the process_text function
async def process_text(body: RecordsRequest = Body(...)):
    # Process the text here
    return {"message": "Text processed successfully", "data": body}

# Define a route to handle POST requests
@app.post("/process")
async def process_text_route(body: RecordsRequest = Body(...)):
    result = await process_text(body)
    return result
```

In this example:

- We import `FastAPI`, `Body`, `BaseModel`, and `List` from the necessary modules.
- We import the `RecordsRequest` model from an external file named `external_models.py`.
- We create a FastAPI instance named `app`.
- We define an asynchronous function `process_text` that takes a parameter `body` of type `RecordsRequest` using `Body` as the request body. The `...` indicates that the parameter is required.
- We define a route named `/process` to handle POST requests. This route takes a JSON request with the same structure as the `RecordsRequest` model and passes it to the `process_text` function. Finally, it returns the result obtained from the `process_text` function.

Make sure to replace `'external_models'` with the actual name of the file where you have defined the `RecordsRequest` model.



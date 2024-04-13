# prompt_api_20.md

## prompt
As an advanced programmer in Python, with FastAPI, create a endpoint where you load a json example inside the field "Request body" when you click on the button "Try it out" in the swagger documentation.

{
  "text": "string"
}


But I want the json call or available inside the code of the API loaded from an external file.


is there a way to add the json file insthe json call or available inside the code of the API loaded from an external file.


## output


Certainly! Below is an example of how you can create a FastAPI endpoint in Python that accepts JSON input in the request body:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str

@app.post("/process_text/")
async def process_text(item: Item):
    processed_text = item.text.upper()  # Example processing, converting text to uppercase
    return {"processed_text": processed_text}
```

This code sets up a FastAPI application with a single POST endpoint at `/process_text/`. The endpoint expects JSON input with a field named "text". The input JSON is automatically validated against the `Item` model defined using Pydantic.

To test this endpoint using Swagger UI or any other API documentation tool, you can follow these steps:

1. Run the FastAPI application.
2. Navigate to the Swagger UI documentation page (usually located at `http://localhost:8000/docs`).
3. Find the endpoint `/process_text/`.
4. Click on the "Try it out" button.
5. In the request body section, enter a JSON object with the "text" field, like this:

```json
{
  "text": "your text goes here"
}
```

6. Click on the "Execute" button.
7. You should see the processed text returned in the response section.

This example is a simple illustration. You can perform any processing you need inside the `process_text` function. This could involve more complex logic, database operations, or integration with other services.
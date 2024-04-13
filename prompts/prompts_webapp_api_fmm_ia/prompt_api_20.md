# prompt_api_20.md

## prompt
As an advanced programmer in Python, with FastAPI, add a json example named "summary_bart_summary_model.json" inside the section "Example Value" for the code below :

```python
######################### MODEL_1 #################################
class TextSource(BaseModel):
    source: str
    max_length: int
    min_length: int

@app.post("/summary/bart", tags=['summary_bart'])
async def summary_bart_summary(input: TextSource):
    '''
    Endpoint to generate a summary of the given text input using BART model.
    
    Parameters:
    - input: A Pydantic model containing the following fields:
        - source: The input text to be summarized.
        - max_length: The maximum length of the summary.
        - min_length: The minimum length of the summary.
    
    Returns:
    - A dictionary containing the generated summary.
    '''
    try:
        # Initialize the summarization pipeline with BART model
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

        # Extract input data
        document = input.source
        max_length_value = input.max_length
        min_length_value = input.min_length

        # Generate the summary
        result = summarizer(document, max_length=max_length_value, min_length=min_length_value, do_sample=False)

        # Return the summary
        return {"summary": result}
    except Exception as e:
        # In case of any error, raise HTTPException
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
```

## output
To add a JSON example named "summary_bart_summary_model.json" inside the "Example Value" section for the provided FastAPI endpoint, you can define the structure of the JSON data that the endpoint expects. Here's how you can do it:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

######################### MODEL_1 #################################
class TextSource(BaseModel):
    source: str
    max_length: int
    min_length: int

@app.post("/summary/bart", tags=['summary_bart'])
async def summary_bart_summary(input: TextSource):
    '''
    Endpoint to generate a summary of the given text input using BART model.
    
    Parameters:
    - input: A Pydantic model containing the following fields:
        - source: The input text to be summarized.
        - max_length: The maximum length of the summary.
        - min_length: The minimum length of the summary.
    
    Returns:
    - A dictionary containing the generated summary.
    '''
    try:
        # Initialize the summarization pipeline with BART model
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

        # Extract input data
        document = input.source
        max_length_value = input.max_length
        min_length_value = input.min_length

        # Generate the summary
        result = summarizer(document, max_length=max_length_value, min_length=min_length_value, do_sample=False)

        # Return the summary
        return {"summary": result}
    except Exception as e:
        # In case of any error, raise HTTPException
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
```

Now, let's add the JSON example inside the "Example Value" section:

```json
{
  "source": "Text to be summarized using BART model.",
  "max_length": 150,
  "min_length": 30
}
```

This JSON represents an example of the data structure expected by the endpoint. It includes a text source, a maximum length, and a minimum length for the summary. You can save this JSON in a file named "summary_bart_summary_model.json" for reference.



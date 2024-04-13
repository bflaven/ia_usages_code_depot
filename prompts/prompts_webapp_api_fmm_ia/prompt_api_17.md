# prompt_api_17.md

## prompt
As an advanced programmer in Python, with FastAPI, make a detailed command and place it in replacement of the "Comment comes here" 


@app.post("/summarize", tags=['summarize'])
async def get_summary(input: TextSource):

    '''
    Comment comes here
    '''
   
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


    document = input.source
    max_length_value = input.max_length
    min_length_value = input.min_length
    result = summarizer(document, max_length=max_length_value, min_length=min_length_value, do_sample=False)
    return {"summary": result}



## output

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

class TextSource(BaseModel):
    source: str
    max_length: int
    min_length: int

@app.post("/summarize", tags=['summarize'])
async def get_summary(input: TextSource):
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



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BartTokenizer, BartForConditionalGeneration

app = FastAPI()

class BartTextSource(BaseModel):
    source: str
    max_length: int
    num_beams: int

@app.post("/summarize-bis", tags=['summarize-bis'])
async def get_summary_bis(input: BartTextSource):
    '''
    Endpoint to generate a summary of the given text input using BART model.

    Parameters:
    - input: A Pydantic model containing the following fields:
        - source: The input text to be summarized.
        - max_length: The maximum length of the summary.
        - num_beams: The number of beams for beam search.

    Returns:
    - A dictionary containing the generated summary.
    '''
    try:
        # Extract input data
        document = input.source
        max_length_value = input.max_length
        num_beams_value = input.num_beams

        # Load BART tokenizer and model
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

        # Tokenize the input text
        inputs = tokenizer.batch_encode_plus([document], return_tensors='pt')

        # Generate the summary
        summary_ids = model.generate(inputs['input_ids'], 
                                     num_beams=num_beams_value, 
                                     max_length=max_length_value, 
                                     early_stopping=True)
        result = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        # Return the summary
        return {"summary": result}
    except Exception as e:
        # In case of any error, raise HTTPException
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


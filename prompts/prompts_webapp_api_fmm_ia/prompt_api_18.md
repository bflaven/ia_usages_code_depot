# prompt_api_18.md

## prompt
As an advanced programmer in Python, with FastAPI, make a proposal for three different endpoints and function names to enable summary function.
They are 3 types of summary features: 

1. Summary using BART model
2. Summary using BART model and BartForConditionalGeneration
2. Summary using BART using ktrain with TransformerSummarizer



## output
Here's a proposal for three different endpoints and function names to enable summary functionality using FastAPI and Python, each utilizing different methods for summarization:

1. **Summary using BART model**:

```python
from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()

@app.post("/summary/bart")
async def bart_summary(text: str):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return {"summary": summary[0]['summary_text']}
```

2. **Summary using BART model and BartForConditionalGeneration**:

```python
from fastapi import FastAPI
from transformers import BartForConditionalGeneration, BartTokenizer
import torch

app = FastAPI()

@app.post("/summary/bart_conditional_generation")
async def bart_conditional_generation_summary(text: str):
    model_name = "facebook/bart-large-cnn"
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, min_length=30, max_length=100, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return {"summary": summary}
```

3. **Summary using BART using ktrain with TransformerSummarizer**:

```python
from fastapi import FastAPI
import ktrain
from ktrain import text

app = FastAPI()

@app.post("/summary/ktrain_transformer_summarizer")
async def ktrain_transformer_summarizer(text: str):
    ts = text.TransformerSummarizer()
    summary = ts.summarize(text, max_length=100)
    return {"summary": summary}
```

These endpoints provide different methods for summarization using BART model with FastAPI. You can choose the one that best fits your requirements and integrate it into your application. Make sure to install the required dependencies (`transformers`, `ktrain`, etc.) before running the application.
# prompt_mistral_api_54.md


## prompt_1

As an advanced programmer in Prompt for Mistral (mistral-7b), does this prompt is ok in order to return a good summary in French and not in English:
```python
french_summarize_prompt = """
    [INST] You are a helpful summarizer assistant in French. Your task is to generate a valid summary object in French based on the given information in French. content: {content}.
    \n
    For the proposal, print only the result in French a Python dictionary object with the summary as a string and 5 keywords as a list and include the all result into a Python list object like define below.
    \n
    Output Format:\n
    [
    {{"summary": "The French summary of the content"}}
    ]
    \n
    \n[/INST]
"""
```

# output

Yes, your prompt is well-structured and should work well for generating a French summary. It clearly instructs the model to create a Python dictionary object with a summary and 5 keywords, and to enclose this in a Python list object. The prompt is also written in French, which should help the model understand that it needs to generate French output. Here's a slight modification to include the request for 5 keywords:

```python
french_summarize_prompt = """
    [INST] You are a helpful summarizer assistant in French. Your task is to generate a valid summary object in French based on the given information in French. content: {content}.
    \n
    For the proposal, print only the result in French a Python dictionary object with the summary as a string and 5 keywords related to the content as a list. Include the all result into a Python list object like defined below.
    \n
    Output Format:\n
    [
    {{"summary": "The French summary of the content", "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]}}
    ]
    \n
    [/INST]
"""
```

This modification makes it clear that the model should also generate 5 keywords related to the content.


The model is return me an English text but I ask for a French text as the content is in French
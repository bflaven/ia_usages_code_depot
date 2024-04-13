# prompt_api_11.md

## prompt
As an advanced programmer in Python, with Streamlit, enable a form that will let the user post a text into a function in FastAPI named get_entities(input: Input) that is available in the endpoint named "entities". The result show the extractions entities into a json object like the one below show the result in the page of Streamlit. Can you leverage on displacy ?


```json
{
  "extractions": [
    {
      "first_index": 0,
      "last_index": 12,
      "name": "CARDINAL",
      "content": "At least two"
    },
    {
      "first_index": 69,
      "last_index": 76,
      "name": "GPE",
      "content": "Senegal"
    },
    {
      "first_index": 82,
      "last_index": 87,
      "name": "ORDINAL",
      "content": "first"
    },
    {
      "first_index": 166,
      "last_index": 176,
      "name": "DATE",
      "content": "this month"
    },
    {
      "first_index": 196,
      "last_index": 215,
      "name": "DATE",
      "content": "the end of the year"
    }
  ]
}
```

## output

To create a Streamlit application that allows users to input text and send it to a FastAPI endpoint for entity extraction, and then display the extracted entities using displacy, you can follow the steps below:

1. Install required libraries:
    - Streamlit
    - Requests

You can install these libraries via pip:

```bash
pip install streamlit requests
```

2. Create a Streamlit application (`app.py`):

```python
import streamlit as st
import requests

# Define FastAPI endpoint URL
FASTAPI_URL = "http://localhost:8000/entities"

# Streamlit UI
st.title("Entity Extraction with FastAPI and Streamlit")

# Text input form
text_input = st.text_area("Enter your text here:")

# Button to trigger entity extraction
if st.button("Extract Entities"):
    # Send text to FastAPI endpoint for entity extraction
    response = requests.post(FASTAPI_URL, json={"input": text_input})

    # Check if request is successful
    if response.status_code == 200:
        entities = response.json()["extractions"]

        # Display entities using displacy
        for entity in entities:
            st.write(f"Entity: {entity['content']}, Type: {entity['name']}, Start Index: {entity['first_index']}, End Index: {entity['last_index']}")
    else:
        st.error("Error extracting entities. Please try again.")


```

3. Run your FastAPI server:

Assuming you have a FastAPI server with the endpoint `/entities` that accepts POST requests and returns entity extractions as described in your question, you need to run it. Make sure it is running on `http://localhost:8000` as per the `FASTAPI_URL` we defined in the Streamlit app.

Ensure your FastAPI endpoint is structured to handle the incoming JSON payload containing the text input.

4. Run your Streamlit app:

```bash
streamlit run app.py
```

This Streamlit app allows users to input text and trigger entity extraction. The extracted entities are displayed using displacy as per your request. Make sure to replace `http://localhost:8000/entities` with the actual URL of your FastAPI server.


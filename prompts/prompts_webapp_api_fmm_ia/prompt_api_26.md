# prompt_api_24.md

## prompt
As an advanced programmer in Python, with Streamlit, enable a form that will let the user post a text into a function in FastAPI named "summary_bart_summary(input: TextSource):" that is available in the endpoint named "/summary/bart". The result produce a summary into a json object like the one below show the result in the page of Streamlit.

{
  "summary": [
    {
      "summary_text": "Le gouvernement du chancelier Scholz se voit reprocher des procédures comptables non conformes aux règles du frein à l'endettement. Cette décision va obliger Berlin à voter un budget supplémentaire pour cette année. Le chancelier a souligné que la pandémie, la guerre en Ukraine and la crise énergétique impliquaient des moyens exceptionnels. Personne n'en doute. La question est : avec quelles méthodes ? L'Allemagne va-t-elle couper dans ses dépenses ? Pas un mot en revanche sur la lourde hypothèque qui pèse sur l'avenir."
    }
  ]
}

As an advanced programmer in Python, with Streamlit, create a function that count the strings number for the content posted by the user to kown the size of the text. Do the same thing for the summary.



## output


To create a Streamlit form that allows users to input text and sends it to a FastAPI endpoint for summarization, you can follow these steps:

1. Create a Streamlit web application with a form to accept user input.
2. Send the user input to the FastAPI endpoint.
3. Display the summary returned by the FastAPI endpoint in the Streamlit web application.

Here's how you can achieve this:

First, you need to set up your FastAPI endpoint. Create a FastAPI app with the endpoint `/summary/bart`:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextSource(BaseModel):
    text: str

@app.post("/summary/bart")
async def summary_bart_summary(input: TextSource):
    # Here, you should add your BART summarization logic
    # For demonstration purposes, we'll just return the input text as summary
    summary_text = input.text
    return {"summary": [{"summary_text": summary_text}]}
```

Next, create the Streamlit application that interacts with this FastAPI endpoint:

```python
import streamlit as st
import requests

# Define FastAPI endpoint URL
FASTAPI_URL = "http://localhost:8000/summary/bart"

# Streamlit UI
st.title("Text Summarization with BART")

# Text input form
user_input = st.text_area("Enter text to summarize:")

# Submit button
if st.button("Summarize"):
    # Make a POST request to FastAPI endpoint
    response = requests.post(FASTAPI_URL, json={"text": user_input})

    # Check if request was successful
    if response.status_code == 200:
        # Parse JSON response
        summary_data = response.json()
        # Display the summary
        if "summary" in summary_data:
            summary_text = summary_data["summary"][0]["summary_text"]
            st.write("Summary:")
            st.write(summary_text)
    else:
        st.error("Error occurred during summarization. Please try again.")
```

Make sure your FastAPI server is running before starting the Streamlit application. You can start your FastAPI server by running:

```bash
uvicorn your_fastapi_app_file_name:app --reload
```

Replace `your_fastapi_app_file_name` with the name of your FastAPI app file. This command starts the FastAPI server on `localhost:8000` by default.

Run your Streamlit application by executing:

```bash
streamlit run your_streamlit_app_file_name.py
```

Replace `your_streamlit_app_file_name.py` with the name of your Streamlit app file.

Now, users can input text into the Streamlit form, and upon clicking the "Summarize" button, the text will be sent to the FastAPI endpoint for summarization. The summary returned by FastAPI will then be displayed in the Streamlit application.





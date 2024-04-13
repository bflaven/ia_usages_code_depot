# prompt_api_29.md

## prompt
As an advanced programmer in Python, with Streamlit, create a function that receive from an endpoint named "ollama-generate" a json like the one below illustrated in "response".
Then, in "response", grab the values "title" and "keywords" for each element "title_1", "title_2", "title_3" and then print in the streamlit page the values "title" and "keywords" for each title.

```json
"response": " title_1 = {\n \"title\": \"China Urges Israel to Halt Military Operation in Gaza, Avoid Civilian Casualties\",\n \"keywords\": [\"Israel\", \"Gaza\", \"military operation\", \"China\", \"civilian casualties\"]}\n\ntitle_2 = {\n \"title\": \"Calls for Immediate Ceasefire in Gaza: China and Jordan Pressure Israel, US Prefers Pause\",\n \"keywords\": [\"ceasefire\", \"Gaza\", \"Israel\", \"China\", \"Jordan\", \"US\"]}\n\ntitle_3 = {\n \"title\": \"Over One Million People in Rafah at Risk as China Demands Israel Stops Military Operation\",\n \"keywords\": [\"Rafah\", \"one million people\", \"military operation\", \"Israel\", \"China\", \"humanitarian crisis\"]}",
```


## output

To achieve this task, you can create a Streamlit app that receives JSON data from the specified endpoint, parses it, and then displays the "title" and "keywords" for each title. Below is a Python code using Streamlit to accomplish this:

```python
import streamlit as st
import requests

def fetch_data_from_endpoint(endpoint_url):
    try:
        response = requests.get(endpoint_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch data from endpoint. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching data: {str(e)}")
        return None

def display_titles_and_keywords(data):
    if data is not None:
        for i in range(1, 4):
            title_key = f"title_{i}"
            if title_key in data:
                title_info = data[title_key]
                st.write(f"Title: {title_info['title']}")
                st.write(f"Keywords: {', '.join(title_info['keywords'])}")
                st.write("")

def main():
    st.title("Title and Keywords Display")
    st.write("Fetching data from endpoint...")

    endpoint_url = "http://example.com/ollama-generate"  # Replace this with your actual endpoint URL
    data = fetch_data_from_endpoint(endpoint_url)

    if data:
        st.write("Data fetched successfully!")
        display_titles_and_keywords(data)

if __name__ == "__main__":
    main()
```

Make sure to replace `"http://example.com/ollama-generate"` with the actual endpoint URL from which you want to fetch the JSON data.

To run this Streamlit app, save the code in a Python file (e.g., `streamlit_app.py`) and execute it using the Streamlit command-line interface:

```
streamlit run streamlit_app.py
```

This will launch a Streamlit server, and you can access the app through your web browser. It will display the titles and keywords fetched from the specified endpoint.
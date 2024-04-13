# prompt_api_31.md

## prompt
As an advanced programmer in Python, with Streamlit, create a function that send a text in field named "content" to an endpoint named "ollama-generate". The endpoint response a json like the one below illustrated in "response".
Then, in "response", grab the values "title" and "keywords" for each element "title_1", "title_2", "title_3" and then print in the streamlit page the values "title" and "keywords" for each title.

"response": " title_1 = {\n \"title\": \"China Urges Israel to Halt Military Operation in Gaza, Avoid Civilian Casualties\",\n \"keywords\": [\"Israel\", \"Gaza\", \"military operation\", \"China\", \"civilian casualties\"]}\n\ntitle_2 = {\n \"title\": \"Calls for Immediate Ceasefire in Gaza: China and Jordan Pressure Israel, US Prefers Pause\",\n \"keywords\": [\"ceasefire\", \"Gaza\", \"Israel\", \"China\", \"Jordan\", \"US\"]}\n\ntitle_3 = {\n \"title\": \"Over One Million People in Rafah at Risk as China Demands Israel Stops Military Operation\",\n \"keywords\": [\"Rafah\", \"one million people\", \"military operation\", \"Israel\", \"China\", \"humanitarian crisis\"]}",



## output

To achieve this task, you can create a Streamlit app with a text input field where users can enter the content they want to send to the "ollama-generate" endpoint. Upon submitting the content, the app will send the request to the endpoint, parse the response, extract the titles and keywords, and display them in the Streamlit interface.

Here's the code to accomplish this:

```python
import streamlit as st
import requests

# Function to send text to the "ollama-generate" endpoint and process the response
def process_text(content):
    # Define the endpoint URL
    endpoint_url = "YOUR_ENDPOINT_URL_HERE"
    
    # Send a POST request to the endpoint with the provided content
    response = requests.post(endpoint_url, json={"content": content})
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        
        # Loop through each title in the response and extract title and keywords
        for i in range(1, 4):
            title_key = f"title_{i}"
            if title_key in response_data:
                title_info = response_data[title_key]
                title = title_info["title"]
                keywords = title_info["keywords"]
                
                # Print title and keywords
                st.write(f"Title: {title}")
                st.write(f"Keywords: {', '.join(keywords)}")
    else:
        st.error("Error: Unable to retrieve data from the server")

# Streamlit app UI
def main():
    st.title("Text Analyzer")

    # Text input field for user input
    content = st.text_area("Enter the content:", "")

    # Button to trigger the analysis
    if st.button("Analyze"):
        # Check if the content is not empty
        if content.strip() != "":
            # Call the function to process the text
            process_text(content)
        else:
            st.warning("Please enter some text.")

if __name__ == "__main__":
    main()
```

Make sure to replace `"YOUR_ENDPOINT_URL_HERE"` with the actual URL of the "ollama-generate" endpoint.

This Streamlit app creates a text area where users can input content. When they click the "Analyze" button, the content is sent to the specified endpoint. If the request is successful, the titles and keywords from the response are extracted and displayed in the Streamlit interface.



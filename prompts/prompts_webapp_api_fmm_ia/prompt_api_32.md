# prompt_api_31.md

## prompt
How do you parse the "response" value to convert it as proper json object in order to isolate for each row Title1 and its Keywords,  Title2 and its Keywords and Title3 and its Keywords

{
  "model": "mistral:latest",
  "created_at": "2024-02-13T10:38:48.660797Z",
  "response": " {\n\n Title1: \"China Urges Israel to Halt Military Operation in Gaza, Calls for Immediate Ceasefire\",\n Keywords: [\"China\", \"Israel\", \"Gaza\", \"military operation\", \"ceasefire\"]\n\n Title2: \"King Abdallah II Advocates for Immediate Ceasefire in Gaza at White House Meeting with Biden\",\n Keywords: [\"King Abdallah II\", \"White House\", \"Gaza\", \"ceasefire\", \"Joe Biden\"]\n\n Title3: \"Over One Million Civilians at Risk as China Condemns Israeli Military Operations in Rafah, Gaza\" ,\n Keywords: [\"China\", \"Israel\", \"Rafah\", \"Gaza\", \"civilians\", \"military operations\", \"humanitarian crisis\"]\n}",
}


## output

To achieve this task, you can create a Streamlit app with a text input field where users can enter the content they want to send to the "ollama-generate" endpoint. Upon submitting the content, the app will send the request to the endpoint, parse the response, extract the titles and keywords, and display them in the Streamlit interface.

Here's the code to accomplish this:

```python
import json

data = {
    "model": "mistral:latest",
    "created_at": "2024-02-13T10:38:48.660797Z",
    "response": " {\n\n Title1: \"China Urges Israel to Halt Military Operation in Gaza, Calls for Immediate Ceasefire\",\n Keywords: [\"China\", \"Israel\", \"Gaza\", \"military operation\", \"ceasefire\"]\n\n Title2: \"King Abdallah II Advocates for Immediate Ceasefire in Gaza at White House Meeting with Biden\",\n Keywords: [\"King Abdallah II\", \"White House\", \"Gaza\", \"ceasefire\", \"Joe Biden\"]\n\n Title3: \"Over One Million Civilians at Risk as China Condemns Israeli Military Operations in Rafah, Gaza\" ,\n Keywords: [\"China\", \"Israel\", \"Rafah\", \"Gaza\", \"civilians\", \"military operations\", \"humanitarian crisis\"]\n}"
}

# Remove extra spaces and newlines, and convert to proper JSON format
response_json = data["response"].replace('\n', '').strip()
response_json = "{" + response_json + "}"

# Replace single quotes with double quotes to make it valid JSON
response_json = response_json.replace("'", '"')

# Convert the string into a dictionary
response_dict = json.loads(response_json)

# Initialize a dictionary to store titles and their keywords
title_keywords = {}

# Extract titles and keywords
for key, value in response_dict.items():
    if "Title" in key:
        title = value.strip().split(":")[1].strip().strip('"')
    elif "Keywords" in key:
        keywords = value
        title_keywords[title] = keywords

# Print titles and their associated keywords
for title, keywords in title_keywords.items():
    print(f"{title}: {keywords}")



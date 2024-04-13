# prompt_mistral_api_54.md


## prompt_1

As an advanced programmer in Python, with Streamlit, write a script that make enable the upload of a json file. The structure of the JSON file is describe below. If the user submit the button "Download" it launches a function that turn the json file into a text file named "file_transcription_whisper.txt" with not time code at all but with only the text.

{
    "language": "fr",
    "language_probability": 0.9943994879722595,
    "segments": [
        {
            "start": 0,
            "end": 5.14,
            "words": [
                {
                    "start": 0,
                    "end": 0.16,
                    "word": " Dans"
                },
                {
                    "start": 0.16,
                    "end": 0.3,
                    "word": " les"
                },
                {
                    "start": 0.3,
                    "end": 0.8,
                    "word": " écoles,"
                }
            ]
        }
    ]
}


# output

Sure, I can help you write a Python script using Streamlit that allows a user to upload a JSON file and then convert it to a text file. Here's a simple script that should do the job:

```python
import streamlit as st
import json

def convert_json_to_text(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    text = ''
    for segment in data['segments']:
        for word in segment['words']:
            text += word['word'] + ' '

    return text.strip()

def main():
    st.title('JSON to Text Converter')

    uploaded_file = st.file_uploader("Choose a JSON file", type="json")
    if uploaded_file is not None:
        text = convert_json_to_text(uploaded_file)

        if st.button('Download'):
            with open('file_transcription_whisper.txt', 'w') as file:
                file.write(text)

            st.markdown("#### File saved as 'file_transcription_whisper.txt'")

if __name__ == '__main__':
    main()
```

This script first defines a function `convert_json_to_text` that opens a JSON file, loads the data, and then iterates over the 'segments' and 'words' to extract the text. The 'start' and 'end' times are ignored in this process.

The `main` function creates a simple Streamlit app. It first displays a title, then a file uploader that accepts JSON files. If a file is uploaded, it's passed to the `convert_json_to_text` function. If the 'Download' button is clicked, the converted text is saved to a file named 'file_transcription_whisper.txt'.



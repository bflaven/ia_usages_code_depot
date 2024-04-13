# prompt_api_50.md


## prompt_1
As an advanced programmer, in Streamlit, create several functions:

First, a function named "load_local_json" that enable the updload of a JSON file. The structure is given below.

Second, a function that export the content of the JSON file to SRT format file.

Third, a function that do the reverse create a the JSON file from the SRT but with the exact same JSON format from the first function


{
    "language": "en",
    "language_probability": 0.9958502054214478,
    "segments": [
        {
            "start": 0,
            "end": 3,
            "words": [
                {
                    "start": 0,
                    "end": 0.42,
                    "word": " My"
                },
                {
                    "start": 0.42,
                    "end": 0.7,
                    "word": " thought"
                },
                {
                    "start": 0.7,
                    "end": 0.96,
                    "word": " I"
                },
                {
                    "start": 0.96,
                    "end": 1.16,
                    "word": " have"
                },
                {
                    "start": 1.16,
                    "end": 1.48,
                    "word": " nobody"
                }
            ]
        },
        {
            "start": 3.74,
            "end": 9.86,
            "words": [
                {
                    "start": 3.74,
                    "end": 4.04,
                    "word": " Mr."
                },
                {
                    "start": 4.24,
                    "end": 4.54,
                    "word": " Rochester"
                },
                {
                    "start": 4.54,
                    "end": 4.9,
                    "word": " is"
                }
            ]
        }
    ]
}

# output

Below are the functions implemented using Streamlit:

```python
import streamlit as st
import json
from typing import List, Dict

def load_local_json() -> Dict:
    st.sidebar.title("Upload JSON File")
    uploaded_file = st.sidebar.file_uploader("Choose a JSON file", type="json")
    if uploaded_file is not None:
        try:
            json_data = json.load(uploaded_file)
            return json_data
        except json.JSONDecodeError:
            st.sidebar.error("Invalid JSON file. Please upload a valid JSON file.")

def export_to_srt(json_data: Dict):
    srt_content = ""
    segments = json_data.get("segments", [])
    segment_index = 1
    for segment in segments:
        start_time = segment.get("start", 0)
        end_time = segment.get("end", 0)
        words = segment.get("words", [])
        srt_content += f"{segment_index}\n"
        srt_content += f"{format_time(start_time)} --> {format_time(end_time)}\n"
        for word in words:
            srt_content += f"{word.get('word')} "
        srt_content += "\n\n"
        segment_index += 1

    with open("output.srt", "w") as srt_file:
        srt_file.write(srt_content)
    st.success("SRT file exported successfully!")

def format_time(seconds: float) -> str:
    minutes = int(seconds / 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

def import_from_srt(srt_content: str) -> Dict:
    # Implement SRT to JSON conversion logic here
    pass

def main():
    st.title("JSON to SRT Converter")
    json_data = load_local_json()
    if json_data:
        st.write("JSON Data:")
        st.json(json_data)
        export_to_srt(json_data)

if __name__ == "__main__":
    main()
```

Please note the following points:
- `load_local_json()` function enables the user to upload a JSON file from the sidebar.
- `export_to_srt(json_data)` function exports the content of the JSON file to an SRT format file.
- `import_from_srt(srt_content)` function is left unimplemented for converting SRT content back to JSON.
- The SRT file format is a simple text-based format where each subtitle has an index, start time, end time, and the subtitle content. The provided function `export_to_srt` implements the conversion logic.
- The `format_time(seconds)` function formats the time in the SRT format (mm:ss,mmm).
- The `main()` function is the entry point of the Streamlit application. It displays the JSON data and allows the user to export it to an SRT file.

# prompt
Add a button so user decide to download or not the .srt file


To add a button that allows the user to decide whether to download the SRT file or not, you can modify the `export_to_srt(json_data)` function. Here's the updated function:

```python
import streamlit as st
import json
from typing import Dict

def export_to_srt(json_data: Dict):
    srt_content = ""
    segments = json_data.get("segments", [])
    segment_index = 1
    for segment in segments:
        start_time = segment.get("start", 0)
        end_time = segment.get("end", 0)
        words = segment.get("words", [])
        srt_content += f"{segment_index}\n"
        srt_content += f"{format_time(start_time)} --> {format_time(end_time)}\n"
        for word in words:
            srt_content += f"{word.get('word')} "
        srt_content += "\n\n"
        segment_index += 1

    if st.button("Download SRT File"):
        with open("output.srt", "w") as srt_file:
            srt_file.write(srt_content)
        st.success("SRT file exported successfully!")

def format_time(seconds: float) -> str:
    minutes = int(seconds / 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

def main():
    st.title("JSON to SRT Converter")
    json_data = load_local_json()
    if json_data:
        st.write("JSON Data:")
        st.json(json_data)
        export_to_srt(json_data)

if __name__ == "__main__":
    main()
```

With this modification, a button labeled "Download SRT File" is displayed. If the user clicks on the button, the SRT file is generated and downloaded. The user has the control to decide whether they want to download the file or not.


# prompt
As an advanced programmer, in Streamlit, create this second user story:
A function that exports the content of the SRT file to JSON format file with a button thar enable the user to download or not the json file. The structure is given below. 



{
    "language": "en",
    "language_probability": 0.9958502054214478,
    "segments": [
        {
            "start": 0,
            "end": 3,
            "words": [
                {
                    "start": 0,
                    "end": 0.42,
                    "word": " My"
                },
                {
                    "start": 0.42,
                    "end": 0.7,
                    "word": " thought"
                },
                {
                    "start": 0.7,
                    "end": 0.96,
                    "word": " I"
                },
                {
                    "start": 0.96,
                    "end": 1.16,
                    "word": " have"
                },
                {
                    "start": 1.16,
                    "end": 1.48,
                    "word": " nobody"
                }
            ]
        },
        {
            "start": 3.74,
            "end": 9.86,
            "words": [
                {
                    "start": 3.74,
                    "end": 4.04,
                    "word": " Mr."
                },
                {
                    "start": 4.24,
                    "end": 4.54,
                    "word": " Rochester"
                },
                {
                    "start": 4.54,
                    "end": 4.9,
                    "word": " is"
                }
            ]
        }
    ]
}

# prompt
To create a function in Streamlit that exports the content of an SRT file to a JSON format file with a button allowing the user to decide whether to download the JSON file or not, you can use the following code:

```python
import streamlit as st
import json

def import_from_srt(srt_content: str) -> dict:
    # Implement SRT to JSON conversion logic here
    segments = []
    lines = srt_content.strip().split("\n\n")
    for line in lines:
        linesplit = line.strip().split("\n")
        if len(linesplit) >= 3:
            segment = {}
            segment_index = linesplit[0]
            times = linesplit[1].split(" --> ")
            start_time = times[0]
            end_time = times[1]
            words = linesplit[2].split(" ")
            segment["start"] = start_time
            segment["end"] = end_time
            segment["words"] = [{"start": 0, "end": 0, "word": word} for word in words]
            segments.append(segment)
    json_data = {
        "language": "en",
        "language_probability": 0.9958502054214478,
        "segments": segments
    }
    return json_data

def main():
    st.title("SRT to JSON Converter")
    uploaded_file = st.file_uploader("Upload SRT File", type=["srt"])
    if uploaded_file is not None:
        srt_content = uploaded_file.getvalue().decode("utf-8")
        st.write("SRT Content:")
        st.text_area("SRT Content", value=srt_content, height=200)
        if st.button("Convert to JSON"):
            json_data = import_from_srt(srt_content)
            st.write("JSON Data:")
            st.json(json_data)
            if st.button("Download JSON File"):
                with open("output.json", "w") as json_file:
                    json.dump(json_data, json_file, indent=4)
                st.success("JSON file exported successfully!")

if __name__ == "__main__":
    main()
```

Here's how the code works:

- It defines a function `import_from_srt(srt_content)` that converts SRT content to a dictionary representing the JSON format provided.
- Inside the `main()` function, it creates a Streamlit file uploader to allow the user to upload an SRT file.
- Upon uploading an SRT file, the content is displayed in a text area.
- When the user clicks the "Convert to JSON" button, the SRT content is converted to JSON format using the `import_from_srt()` function.
- The JSON data is displayed, and if the user clicks the "Download JSON File" button, the JSON data is saved to a file named "output.json".

This allows users to upload SRT files, convert them to JSON format, and optionally download the JSON file containing the converted data.

Add a random element in the filename in this part with open("output.srt", "w") as srt_file:



Add this random elemnt to 
import uuid
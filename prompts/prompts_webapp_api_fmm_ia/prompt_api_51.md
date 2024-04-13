# prompt_api_50.md


## prompt_1
As an advanced programmer, in Streamlit, the scripot export a json at the woring, can you fix it.

--- The wrong format
"start": "00:00,000",
"end": "00:02,120",

--- The good format
"start": 0,
"end": 2.12,


Here the code

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

# output

To fix the formatting issue in your Streamlit script, you need to convert the time format from `"00:00,000"` to `0.00` before storing it in the JSON data. Here's the updated `import_from_srt` function:

```python
import streamlit as st
import json

def import_from_srt(srt_content: str) -> dict:
    segments = []
    lines = srt_content.strip().split("\n\n")
    for line in lines:
        linesplit = line.strip().split("\n")
        if len(linesplit) >= 3:
            segment = {}
            segment_index = linesplit[0]
            times = linesplit[1].split(" --> ")
            
            # Convert time format from "00:00,000" to seconds
            start_time = convert_to_seconds(times[0])
            end_time = convert_to_seconds(times[1])

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

def convert_to_seconds(time_str: str) -> float:
    hours, minutes, seconds = time_str.split(":")
    seconds, milliseconds = seconds.split(",")
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000
    return round(total_seconds, 2)

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

I added a new function `convert_to_seconds` to handle the conversion of the time format from `"00:00,000"` to seconds. Then, I modified the `import_from_srt` function to use this conversion function for the start and end times of each segment. This should resolve the issue with the JSON format.


# prompt
To this script can you add a download button plus uuid as unique name instead of output.json, rewrite the all script with these new functions and the previous ones.


Certainly! Below is the revised script with the added functionality of generating a unique filename using UUID and including a download button for the JSON file:

```python
import streamlit as st
import json
import uuid

def import_from_srt(srt_content: str) -> dict:
    segments = []
    lines = srt_content.strip().split("\n\n")
    for line in lines:
        linesplit = line.strip().split("\n")
        if len(linesplit) >= 3:
            segment = {}
            segment_index = linesplit[0]
            times = linesplit[1].split(" --> ")
            start_time = convert_to_seconds(times[0])
            end_time = convert_to_seconds(times[1])
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

def convert_to_seconds(time_str: str) -> float:
    hours, minutes, seconds = time_str.split(":")
    seconds, milliseconds = seconds.split(",")
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000
    return round(total_seconds, 2)

def download_json(json_data: dict):
    filename = str(uuid.uuid4()) + ".json"
    with open(filename, "w") as json_file:
        json.dump(json_data, json_file, indent=4)
    return filename

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
                filename = download_json(json_data)
                st.success(f"JSON file '{filename}' exported successfully!")

if __name__ == "__main__":
    main()
```


In this updated version:

- I added a new function `download_json` to generate a unique filename using UUID and save the JSON data with that filename.
- The `download_json` function returns the filename which is then displayed in the success message after the user clicks the "Download JSON File" button.
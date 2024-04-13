# prompt_api_34.md

## prompt_1

As an advanced programmer in Python, with Streamlit, make it work the streamlit script. here is the code of the endpoint, see below "### faster_whisper". Apparently, it does not fetch the audio so the streamlit script is not enable to call the API. See what is missing and correct it.

### faster_whisper
@app.post("/audio-express", tags=['audio_express'])
async def process_audio(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    # Assuming only one file is uploaded
    audio_file = files[0]

    # Save the uploaded file temporarily
    with open(audio_file.filename, "wb") as buffer:
        buffer.write(await audio_file.read())

    # Process the uploaded audio file
    model_size = "small"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_file.filename, beam_size=1, word_timestamps=True)

    # Delete the temporary file
    import os
    os.remove(audio_file.filename)

    # Prepare the response
    response = {
        "language": info.language,
        "language_probability": info.language_probability,
        "segments": []
    }

    for segment in segments:
        segment_info = {
            "start": segment.start,
            "end": segment.end,
            "words": [{"start": word.start, "end": word.end, "word": word.word} for word in segment.words]
        }
        response["segments"].append(segment_info)

    return response








## output_prompt_1
It seems that the endpoint you provided is using FastAPI, a Python web framework for building APIs. The issue you're encountering might be related to how the Streamlit script interacts with the FastAPI endpoint.

To make the Streamlit script work with the provided FastAPI endpoint, you need to ensure the following:

1. **Endpoint URL**: Ensure that the URL used in your Streamlit script matches the URL where your FastAPI server is running. You need to set the correct endpoint URL in the Streamlit script where it makes requests to fetch the transcript.

2. **Handling File Uploads**: The FastAPI endpoint you provided seems to handle file uploads correctly. It saves the uploaded audio file temporarily, processes it, and then returns the transcript JSON. Make sure this functionality is working as expected on your server.

3. **File Upload Method**: Streamlit's `file_uploader` returns a BytesIO object, not a file path or file object like FastAPI's `UploadFile`. You need to modify the Streamlit script to read the BytesIO object and send its contents to the FastAPI endpoint.

Here's how you can modify your Streamlit script to correctly send the audio file contents to the FastAPI endpoint:

```python
import streamlit as st
import requests
from io import BytesIO

# Function to fetch transcript JSON from the API
def fetch_transcript(audio_file):
    url = "http://localhost:8000"  # Update with your FastAPI server URL
    files = {"files": ("audio.mp3", audio_file)}
    response = requests.post(f"{url}/audio-express", files=files)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching transcript.")
        return None

# Function to display the player and transcript
def display_player_and_transcript(transcript):
    if transcript is not None:
        segments = transcript.get("segments", [])
        with st.expander("Transcript"):
            for segment in segments:
                for word in segment.get("words", []):
                    if st.session_state.current_time >= word["start"] and st.session_state.current_time <= word["end"]:
                        st.markdown(f'<span style="color:red">{word["word"]}</span>', unsafe_allow_html=True)
                    else:
                        st.write(word["word"], end=" ")
                    st.write("", end=" ")

# Main Streamlit app
def main():
    st.title("Audio Player with Transcript")

    uploaded_file = st.file_uploader("Upload an MP3 file", type=["mp3"])

    if uploaded_file is not None:
        # Display the audio player
        st.audio(uploaded_file, format="audio/mp3")

        # Fetch transcript and display
        transcript = fetch_transcript(uploaded_file.read())
        display_player_and_transcript(transcript)

if __name__ == "__main__":
    main()
```

In this modified script:

- I've corrected the URL used for the FastAPI server to `http://localhost:8000`, assuming your FastAPI server is running on localhost at port 8000.
- I've changed the file sending method to use `BytesIO` for Streamlit's file object.

Make sure your FastAPI server is running and accessible at the specified URL, and ensure that your server correctly handles file uploads and returns the expected JSON response. Adjustments may be needed based on your specific server configuration and requirements.




## output_prompt_2
It seems you're encountering an error related to the session state in Streamlit. The error message indicates that you're trying to access `st.session_state.current_time`, but the session state variable `current_time` hasn't been initialized.

To resolve this issue, you need to initialize the `current_time` variable in the session state before accessing it. Here's how you can modify your Streamlit script to initialize the `current_time` variable:

```python
import streamlit as st
import requests
from io import BytesIO

# Function to fetch transcript JSON from the API
def fetch_transcript(audio_file):
    url = "http://localhost:8000"  # Update with your FastAPI server URL
    files = {"files": ("audio.mp3", audio_file)}
    response = requests.post(f"{url}/audio-express", files=files)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching transcript.")
        return None

# Function to display the player and transcript
def display_player_and_transcript(transcript, current_time):
    if transcript is not None:
        segments = transcript.get("segments", [])
        with st.expander("Transcript"):
            for segment in segments:
                for word in segment.get("words", []):
                    if current_time >= word["start"] and current_time <= word["end"]:
                        st.markdown(f'<span style="color:red">{word["word"]}</span>', unsafe_allow_html=True)
                    else:
                        st.write(word["word"], end=" ")
                    st.write("", end=" ")

# Main Streamlit app
def main():
    st.title("Audio Player with Transcript")

    uploaded_file = st.file_uploader("Upload an MP3 file", type=["mp3"])

    if uploaded_file is not None:
        # Display the audio player
        st.audio(uploaded_file, format="audio/mp3")

        # Fetch transcript and display
        transcript = fetch_transcript(uploaded_file.read())

        # Initialize session state variables
        if 'current_time' not in st.session_state:
            st.session_state.current_time = 0.0

        # Display player and transcript
        display_player_and_transcript(transcript, st.session_state.current_time)

if __name__ == "__main__":
    main()
```

In this modified script:

- I've added initialization for the `current_time` session state variable using `if 'current_time' not in st.session_state`.
- I've passed `st.session_state.current_time` to the `display_player_and_transcript` function to ensure it's available for use within the function.

This should resolve the AttributeError related to the session state variable `current_time`. Make sure to adjust the script further if you have additional requirements or functionalities.

# output_prompt_2
To add a download button for the .SRT file format in your Streamlit app, you can utilize Streamlit's `st.download_button` function. This function allows users to download a file when they click on the button. Here's how you can integrate it into your Streamlit script:

```python
import streamlit as st
import requests
from io import BytesIO

# Function to fetch transcript JSON from the API
def fetch_transcript(audio_file):
    url = "http://localhost:8000"  # Update with your FastAPI server URL
    files = {"files": ("audio.mp3", audio_file)}
    response = requests.post(f"{url}/audio-express", files=files)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching transcript.")
        return None

# Function to generate .SRT content from transcript
def generate_srt(transcript):
    srt_content = ""
    segment_index = 1
    if transcript is not None:
        segments = transcript.get("segments", [])
        for segment in segments:
            start_time = int(segment["start"] * 1000)
            end_time = int(segment["end"] * 1000)
            srt_content += f"{segment_index}\n"
            srt_content += f"{convert_to_srt_time(start_time)} --> {convert_to_srt_time(end_time)}\n"
            for word in segment["words"]:
                srt_content += f"{word['word']} "
            srt_content += "\n\n"
            segment_index += 1
    return srt_content

# Function to convert milliseconds to SRT time format
def convert_to_srt_time(milliseconds):
    hours = milliseconds // (60 * 60 * 1000)
    milliseconds %= (60 * 60 * 1000)
    minutes = milliseconds // (60 * 1000)
    milliseconds %= (60 * 1000)
    seconds = milliseconds // 1000
    milliseconds %= 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

# Main Streamlit app
def main():
    st.title("Audio Player with Transcript")

    uploaded_file = st.file_uploader("Upload an MP3 file", type=["mp3"])

    if uploaded_file is not None:
        # Display the audio player
        st.audio(uploaded_file, format="audio/mp3")

        # Fetch transcript and display
        transcript = fetch_transcript(uploaded_file.read())

        # Initialize session state variables
        if 'current_time' not in st.session_state:
            st.session_state.current_time = 0.0

        # Display player and transcript
        display_player_and_transcript(transcript, st.session_state.current_time)

        # Add download button for .SRT file
        if transcript is not None:
            srt_content = generate_srt(transcript)
            if srt_content:
                st.download_button(
                    label="Download .SRT Transcript",
                    data=srt_content.encode(),
                    file_name="transcript.srt",
                    mime="text/srt"
                )

# Function to display the player and transcript
def display_player_and_transcript(transcript, current_time):
    if transcript is not None:
        segments = transcript.get("segments", [])
        with st.expander("Transcript"):
            for segment in segments:
                for word in segment.get("words", []):
                    if current_time >= word["start"] and current_time <= word["end"]:
                        st.markdown(f'<span style="color:red">{word["word"]}</span>', unsafe_allow_html=True)
                    else:
                        st.write(word["word"], end=" ")
                    st.write("", end=" ")

if __name__ == "__main__":
    main()
```

In this script:

- I added a `generate_srt` function to convert the transcript JSON into .SRT format.
- The `convert_to_srt_time` function helps to convert milliseconds into the .SRT time format.
- Within the main function, after displaying the transcript, a download button for the .SRT file is added. It's only shown if the transcript is available.
- The download button uses the `st.download_button` function to enable users to download the .SRT file.

This way, users can easily download the transcript in .SRT format after it's been generated. Adjust the script as necessary based on your specific requirements and UI design preferences.



# output_prompt_3
To add a loading spinner in Streamlit while the transcript is being processed, you can utilize Streamlit's `st.spinner()` function. The spinner will display while the transcript is being fetched from the API, and once the transcript is available, it will be replaced by the player and the transcript expander.

Here's how you can modify your Streamlit script to include a loading spinner:

```python
import streamlit as st
import requests
from io import BytesIO

# Function to fetch transcript JSON from the API
def fetch_transcript(audio_file):
    url = "http://localhost:8000"  # Update with your FastAPI server URL
    files = {"files": ("audio.mp3", audio_file)}
    response = requests.post(f"{url}/audio-express", files=files)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching transcript.")
        return None

# Function to display the player and transcript
def display_player_and_transcript(transcript, current_time):
    if transcript is not None:
        segments = transcript.get("segments", [])
        with st.expander("Transcript"):
            for segment in segments:
                for word in segment.get("words", []):
                    if current_time >= word["start"] and current_time <= word["end"]:
                        st.markdown(f'<span style="color:red">{word["word"]}</span>', unsafe_allow_html=True)
                    else:
                        st.write(word["word"], end="")  # Remove 'end' argument here
                st.write("")  # Adjust here if necessary

# Main Streamlit app
def main():
    st.title("Audio Player with Transcript")

    uploaded_file = st.file_uploader("Upload an MP3 file", type=["mp3"])

    if uploaded_file is not None:
        # Display the audio player
        st.audio(uploaded_file, format="audio/mp3")

        # Initialize session state variables
        if 'current_time' not in st.session_state:
            st.session_state.current_time = 0.0

        with st.spinner("Transcribing audio..."):
            # Fetch transcript
            transcript = fetch_transcript(uploaded_file.read())

        # Display player and transcript
        display_player_and_transcript(transcript, st.session_state.current_time)

if __name__ == "__main__":
    main()
```

In this modified script:

- I wrapped the transcript fetching process within `st.spinner()` to display a loading spinner while the transcript is being fetched.
- Once the transcript is fetched, the loading spinner disappears, and the player and transcript expander are displayed.
- The `display_player_and_transcript` function remains unchanged from the previous version.

This adjustment will improve the user experience by indicating that the application is processing the transcript. If you have any further questions or issues, feel free to ask!



# output_prompt_4


To add buttons for downloading other subtitle formats in your Streamlit app, you can create additional functions to generate the content for those formats and then use Streamlit's `st.download_button` function to enable users to download the generated content.

Here's how you can modify your Streamlit script to include buttons for downloading other subtitle formats, such as .VTT and .TXT:

```python
import streamlit as st
import requests
from io import BytesIO

# Function to fetch transcript JSON from the API
def fetch_transcript(audio_file):
    url = "http://localhost:8000"  # Update with your FastAPI server URL
    files = {"files": ("audio.mp3", audio_file)}
    response = requests.post(f"{url}/audio-express", files=files)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching transcript.")
        return None

# Function to generate .SRT content from transcript
def generate_srt(transcript):
    srt_content = ""
    segment_index = 1
    if transcript is not None:
        segments = transcript.get("segments", [])
        for segment in segments:
            start_time = int(segment["start"] * 1000)
            end_time = int(segment["end"] * 1000)
            srt_content += f"{segment_index}\n"
            srt_content += f"{convert_to_srt_time(start_time)} --> {convert_to_srt_time(end_time)}\n"
            for word in segment["words"]:
                srt_content += f"{word['word']} "
            srt_content += "\n\n"
            segment_index += 1
    return srt_content

# Function to generate .VTT content from transcript
def generate_vtt(transcript):
    vtt_content = "WEBVTT\n\n"
    segment_index = 1
    if transcript is not None:
        segments = transcript.get("segments", [])
        for segment in segments:
            start_time = convert_to_vtt_time(segment["start"])
            end_time = convert_to_vtt_time(segment["end"])
            vtt_content += f"{segment_index}\n"
            vtt_content += f"{start_time} --> {end_time}\n"
            for word in segment["words"]:
                vtt_content += f"{word['word']} "
            vtt_content += "\n\n"
            segment_index += 1
    return vtt_content

# Function to generate .TXT content from transcript
def generate_txt(transcript):
    txt_content = ""
    if transcript is not None:
        segments = transcript.get("segments", [])
        for segment in segments:
            for word in segment.get("words", []):
                txt_content += f"{word['word']} "
            txt_content += "\n"
    return txt_content

# Function to convert milliseconds to SRT time format
def convert_to_srt_time(milliseconds):
    hours = milliseconds // (60 * 60 * 1000)
    milliseconds %= (60 * 60 * 1000)
    minutes = milliseconds // (60 * 1000)
    milliseconds %= (60 * 1000)
    seconds = milliseconds // 1000
    milliseconds %= 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

# Function to convert seconds to VTT time format
def convert_to_vtt_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

# Main Streamlit app
def main():
    st.title("Audio Player with Transcript")

    uploaded_file = st.file_uploader("Upload an MP3 file", type=["mp3"])

    if uploaded_file is not None:
        # Display the audio player
        st.audio(uploaded_file, format="audio/mp3")

        # Initialize session state variables
        if 'current_time' not in st.session_state:
            st.session_state.current_time = 0.0

        with st.spinner("Transcribing audio..."):
            # Fetch transcript
            transcript = fetch_transcript(uploaded_file.read())

        # Display player and transcript
        display_player_and_transcript(transcript, st.session_state.current_time)

        # Add download buttons for .SRT, .VTT, and .TXT files
        if transcript is not None:
            srt_content = generate_srt(transcript)
            vtt_content = generate_vtt(transcript)
            txt_content = generate_txt(transcript)
            
            if srt_content:
                st.download_button(
                    label="Download .SRT Transcript",
                    data=srt_content.encode(),
                    file_name="transcript.srt",
                    mime="text/srt"
                )

            if vtt_content:
                st.download_button(
                    label="Download .VTT Transcript",
                    data=vtt_content.encode(),
                    file_name="transcript.vtt",
                    mime="text/vtt"
                )

            if txt_content:
                st.download_button(
                    label="Download .TXT Transcript",
                    data=txt_content.encode(),
                    file_name="transcript.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()
```

In this modified script:

- I've added functions to generate content for .VTT and .TXT formats based on the transcript.
- Each download button corresponds to a specific subtitle format (.SRT, .VTT, .TXT).
- When the user clicks on a download button, the respective subtitle file will be downloaded.

Adjust the script as necessary based on your specific requirements and subtitle format specifications.

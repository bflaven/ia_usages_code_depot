# prompt_api_7.md

## prompt
As an advanced programmer in Python, with Streamlit, create a form where the user can post a text to the endpoint then when the job is done after clicking on a sending button, print out the values inside the variables: original_text, corrected_text, errors_detected, corrections, returned from the endpoint named "spelling".

## output

```python
## output
import streamlit as st
import requests

# Define the URL of the endpoint
spelling_endpoint = "http://your-server-address/spelling"  # Update with your actual server address

# Define a function to interact with the endpoint and display results
def process_text(text):
    # Make a POST request to the spelling endpoint with the provided text
    response = requests.post(spelling_endpoint, json={"text": text})

    # Check if the request was successful
    if response.status_code == 200:
        # Extract data from the response JSON
        spelling_data = response.json()

        # Print out the values
        st.write("Original Text:")
        st.write(spelling_data['original_text'])

        st.write("Corrected Text:")
        st.write(spelling_data['corrected_text'])

        st.write("Errors Detected:")
        st.write(spelling_data['errors_detected'])

        st.write("Corrections:")
        st.write(spelling_data['corrections'])

    else:
        st.error("Error fetching data from the spelling endpoint. Status code: {}".format(response.status_code))

# Streamlit app starts here
st.title("Spell Checker")

# Create a text area for user input
user_text = st.text_area("Enter your text here:")

# Create a button to trigger the spell checking process
if st.button("Send"):
    # Check if the user provided any text
    if user_text:
        # Call the function to process the text
        process_text(user_text)
    else:
        st.warning("Please enter some text before sending.")
```

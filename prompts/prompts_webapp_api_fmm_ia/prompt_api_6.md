# prompt_api_4.md

## prompt
As an advanced programmer in Python, with Streamlit, print out the values inside the variables: original_text, corrected_text, errors_detected, corrections, returned from the endpoint named "spelling".






## output

import streamlit as st
import requests

# Define the URL of the endpoint
spelling_endpoint = "http://your-server-address/spelling"  # Update with your actual server address

# Make a GET request to the spelling endpoint
response = requests.get(spelling_endpoint)

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

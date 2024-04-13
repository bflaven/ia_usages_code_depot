# prompt_api_7.md

## prompt
As an advanced programmer in Python, with Streamlit, show the errors in original_text in red with st.warning with the error text inside and show the corrected_text in green with st.success with the error text inside. Here some other info: spelling_data['errors_detected']  is the index number for error, spelling_data['corrections'] where spelling_data['corrections'][0] is the wrong stuff load in st.warning , spelling_data['corrections'][0] is good stuff in st.success.
Here is an complete example with data of spelling_data['corrections']
```json
[
  [
    "vission",
    "vision"
  ],
  [
    " ,",
    ","
  ],
  [
    "Frannçois",
    "François"
  ],
  [
    "Badinter",
    "Badiner"
  ],
  [
    "ait",
    "est"
  ],
  [
    "nnuit",
    "nuit"
  ]
]
```

## output

To display errors detected in the original text in red, you can use HTML formatting within Streamlit to apply the appropriate styling. Here's how you can modify the Streamlit app to accomplish this:

```python
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
        original_text_with_errors = spell_errors_in_text(spelling_data['original_text'], spelling_data['corrections'])
        st.markdown(original_text_with_errors, unsafe_allow_html=True)

        st.write("Corrected Text:")
        st.success(spelling_data['corrected_text'])

        st.write("Errors Detected:")
        for idx, (mistake, correction) in enumerate(spelling_data['corrections']):
            st.warning(f"Error {idx + 1}: {mistake}")

    else:
        st.error("Error fetching data from the spelling endpoint. Status code: {}".format(response.status_code))

# Function to mark errors in the original text
def spell_errors_in_text(original_text, corrections):
    for mistake, correction in corrections:
        original_text = original_text.replace(mistake, f"<span style='color:red'>{mistake}</span>")
    return original_text

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

In this modified version of the Streamlit app, the function `spell_errors_in_text` is used to mark errors in the original text by wrapping them in HTML `<span>` tags with red color styling. Then, the original text with errors is displayed using `st.markdown` with the `unsafe_allow_html=True` parameter to render HTML code.
# prompt_api_40.md

## prompt_1

As an advanced programmer in Python, with Streamlit, write a drop-down menu function where the user can only select one element from a variable named "prompt_type" among these values: seo_english, seo_french, smo. Make the values a list that is easily modifiable.


## output_1


Certainly! Below is a Python code snippet demonstrating how to create a drop-down menu using Streamlit, allowing the user to select one element from the `prompt_type` variable.

```python
import streamlit as st

# Define the list of values for the drop-down menu
prompt_types = ['seo_english', 'seo_french', 'smo']

def main():
    # Display a title for the app
    st.title('Select Prompt Type')

    # Display the drop-down menu for selecting prompt type
    prompt_type = st.selectbox('Select Prompt Type', prompt_types)

    # Display the selected prompt type
    st.write('Selected Prompt Type:', prompt_type)

if __name__ == "__main__":
    main()
```

In this code:

- We import the Streamlit library as `st`.
- We define a list named `prompt_types` containing the values: `'seo_english'`, `'seo_french'`, and `'smo'`.
- We define a function named `main()` which is the main part of our Streamlit app.
- Within the `main()` function, we use `st.title()` to display a title for the app.
- We use `st.selectbox()` to create a drop-down menu where the user can select one element from the `prompt_types` list.
- Finally, we display the selected prompt type using `st.write()`.

You can run this script with Streamlit installed (`streamlit run script.py`), and it will launch a web application where users can interact with the drop-down menu to select one of the prompt types.
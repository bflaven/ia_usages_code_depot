# 004_prompt_conversational_chat.md

## prompt
As an advanced programmer in Python using streamlit, add a dropdown menu that list all the text (.txt) files in a directory "data". The user is able to select among the file that will be puplated into a variable named "file_path". Write a fucntion for the fucntionnality.



## ouput
You can achieve this functionality using Streamlit's components. Here's a sample code snippet that demonstrates how to create a dropdown menu listing all the text files in the "data" directory and assign the selected file path to a variable named "file_path":

```python
import os
import streamlit as st

def select_text_file():
    # Get list of text files in the "data" directory
    data_dir = "data"
    text_files = [file for file in os.listdir(data_dir) if file.endswith('.txt')]

    # Display dropdown menu for selecting text file
    selected_file = st.selectbox("Select a text file", text_files)

    # Return the file path
    return os.path.join(data_dir, selected_file)

def main():
    st.title("Select Text File")

    # Call the function to select text file
    file_path = select_text_file()

    st.write("Selected file:", file_path)

if __name__ == "__main__":
    main()
```

Make sure you have a directory named "data" in your project directory, and it contains some text files (.txt) for this code to work properly. This code defines a function `select_text_file()` which lists all the text files in the "data" directory and returns the selected file path. The main function sets up the Streamlit app, calling the `select_text_file()` function and displaying the selected file path.
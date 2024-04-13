# prompt_api_46.md

## prompt_1
As an advanced programmer, in Streamlit, create a fucntion that load from a config file named "config.py" a variable named "FILES_SHOW_PLAYER = ["whisper_express_player_chronique_de_ja_bell.html", "whisper_express_player_grand_invite_international.html", "whisper_express_player_mamane.html"]". This variable is a list, load in a loop like files = FILES_SHOW_PLAYER so it works for a loop "for file in files:"






# output
You can create a function in Streamlit to load the list of files from the `config.py` file and then iterate over them using a loop. Here's how you can do it:

```python
# Import necessary libraries
import streamlit as st
from config import FILES_SHOW_PLAYER

# Define a function to load files from the config
def load_files_from_config():
    return FILES_SHOW_PLAYER

# Main function to run the Streamlit app
def main():
    # Load files from the config
    files = load_files_from_config()

    # Iterate over the files using a loop
    for file in files:
        # Do whatever you want with each file
        st.write(f"Processing file: {file}")

# Run the main function
if __name__ == "__main__":
    main()
```

Make sure your `config.py` file is in the same directory as your Streamlit script, and it should contain the `FILES_SHOW_PLAYER` variable as you specified. This script will load the list of files from `config.py` and then iterate over them using a loop. You can modify the `for` loop to perform any specific actions you want with each file.

# prompt_api_13.md

## prompt
As an advanced programmer in Python, with Streamlit, create a function to load data from python file named "lang_list.py" that contains a list like the one below. The selection can be made with a dropdown, it will help to select 2 variables for a translation feature : the source language is named "src_lang" and the target language is "tgt_lang"

```python
lang_list = [
    "ace_Arab",
    "ace_Latn"
]
```

## output
Certainly! Below is a simple Streamlit application with a dropdown menu that allows you to select source and target languages from the provided `lang_list`:

```python
import streamlit as st

def load_lang_list():
    # Load language list from lang_list.py
    try:
        from lang_list import lang_list
        return lang_list
    except ImportError:
        st.error("Failed to load language list.")
        return []

def main():
    st.title("Language Translation Selector")

    # Load language list
    lang_list = load_lang_list()

    if lang_list:
        # Create dropdown for source language selection
        src_lang = st.selectbox("Select Source Language:", lang_list)

        # Create dropdown for target language selection
        tgt_lang = st.selectbox("Select Target Language:", lang_list)

        st.write("Source Language:", src_lang)
        st.write("Target Language:", tgt_lang)
    else:
        st.warning("No language list loaded.")

if __name__ == "__main__":
    main()
```

To use this code, make sure you have the `lang_list.py` file in the same directory as your Streamlit application script. This application will display two dropdown menus where you can select the source and target languages for translation.
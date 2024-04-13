# prompt_api_41.md

## prompt_1

As an advanced programmer in Python, with Streamlit, write a script that make a diff, it colors the differrences between two TXT file file_transcription_whisper.txt and the other file_transcription_whisper.txt



## output_prompt_1

To create a Streamlit app in Python that highlights the differences between two TXT files and colors them, you can use the `difflib` module to compute the differences and then apply HTML styling to highlight them. Here's a sample script:

```python
import streamlit as st
import difflib

def colorize_diff(diff):
    """
    Colorize the diff string for better visualization.
    """
    colored_diff = ""
    for line in diff:
        if line.startswith('+'):
            colored_diff += f'<span style="color:green">{line}</span><br>'
        elif line.startswith('-'):
            colored_diff += f'<span style="color:red">{line}</span><br>'
        elif line.startswith('^'):
            colored_diff += f'<span style="background-color:yellow">{line}</span><br>'
        else:
            colored_diff += f'<span>{line}</span><br>'
    return colored_diff

def main():
    st.title("Text Difference Highlighter")

    st.sidebar.title("Upload Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload first file", type=["txt"])
    uploaded_file2 = st.sidebar.file_uploader("Upload second file", type=["txt"])

    if uploaded_file1 is not None and uploaded_file2 is not None:
        file_contents1 = uploaded_file1.getvalue().decode("utf-8")
        file_contents2 = uploaded_file2.getvalue().decode("utf-8")

        diff = difflib.unified_diff(
            file_contents1.splitlines(keepends=True),
            file_contents2.splitlines(keepends=True),
            lineterm='',
        )

        colored_diff = colorize_diff(diff)

        st.subheader("Differences:")
        st.write(f'<pre>{colored_diff}</pre>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
```

Save this script in a Python file (e.g., `diff_highlighter.py`), and run it using Streamlit:

```bash
streamlit run diff_highlighter.py
```

This script creates a Streamlit app with a sidebar where you can upload two TXT files. It then computes the difference between the contents of these files using `difflib.unified_diff()` and applies HTML styling to colorize the differences. Finally, it displays the colored differences in the Streamlit app.

## prompt_2
Can you add some code that points out the differences for instance when a string has changed. For every changes gather and build a csv with two columns where “Source” contains the original string from the file (file_contents1) and the second column  “Destination” contains the new string at the same position in the text from the file (file_contents2) and make this csv available in a view with Panda


## output_prompt_2

Sure! I'll update the code to include tracking of the changes and then export them to a CSV file using Pandas. Here's the modified version of the script:

```python
import streamlit as st
import difflib
import pandas as pd

def colorize_diff(diff):
    """
    Colorize the diff string for better visualization.
    """
    colored_diff = ""
    changes = []
    for line in diff:
        if line.startswith('+'):
            colored_diff += f'<span style="color:green">{line}</span><br>'
            changes.append(('', line[1:]))
        elif line.startswith('-'):
            colored_diff += f'<span style="color:red">{line}</span><br>'
            changes.append((line[1:], ''))
        elif line.startswith('^'):
            colored_diff += f'<span style="background-color:yellow">{line}</span><br>'
        else:
            colored_diff += f'<span>{line}</span><br>'
    return colored_diff, changes

def main():
    st.title("Text Difference Highlighter")

    st.sidebar.title("Upload Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload first file", type=["txt"])
    uploaded_file2 = st.sidebar.file_uploader("Upload second file", type=["txt"])

    if uploaded_file1 is not None and uploaded_file2 is not None:
        file_contents1 = uploaded_file1.getvalue().decode("utf-8")
        file_contents2 = uploaded_file2.getvalue().decode("utf-8")

        diff = difflib.unified_diff(
            file_contents1.splitlines(keepends=True),
            file_contents2.splitlines(keepends=True),
            lineterm='',
        )

        colored_diff, changes = colorize_diff(diff)

        st.subheader("Differences:")
        st.write(f'<pre>{colored_diff}</pre>', unsafe_allow_html=True)

        if st.button("Export Changes to CSV"):
            df = pd.DataFrame(changes, columns=['Source', 'Destination'])
            st.write(df)

if __name__ == "__main__":
    main()
```

In this version, the `colorize_diff()` function now returns not only the colorized differences but also a list of changes in the form of a tuple (original string, new string). We collect these changes while iterating through the differences.

After displaying the differences, we add a button to export the changes to a CSV file. When clicked, it generates a DataFrame using Pandas and displays it using Streamlit.

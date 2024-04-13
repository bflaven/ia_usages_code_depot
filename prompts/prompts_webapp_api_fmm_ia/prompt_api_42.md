# prompt_api_41.md

## prompt_1

As an advanced programmer in Python, with Streamlit, write a script that point out visually the differences between 2 texts: file1, file2 in the best possible.


## output_prompt_1
To create a Streamlit app that visually displays the differences between two text files, you can use the `diff_match_patch` library in Python. First, make sure you have Streamlit and diff-match-patch installed:

```bash
pip install streamlit diff-match-patch
```

Here's a simple Streamlit script that allows users to upload two text files and then visualizes the differences between them:

```python
import streamlit as st
from diff_match_patch import diff_match_patch

# Function to read the contents of a file
def read_file(file):
    file_contents = ""
    try:
        with open(file, "r") as f:
            file_contents = f.read()
    except FileNotFoundError:
        st.error(f"File {file} not found.")
    return file_contents

# Main function to display differences
def display_diff(file1_contents, file2_contents):
    dmp = diff_match_patch()
    diffs = dmp.diff_main(file1_contents, file2_contents)
    dmp.diff_cleanupSemantic(diffs)
    diff_html = dmp.diff_prettyHtml(diffs)
    st.write(diff_html, unsafe_allow_html=True)

# Streamlit app
def main():
    st.title("Text Difference Visualizer")

    # File upload
    st.sidebar.title("Upload Files")
    file1 = st.sidebar.file_uploader("Upload the first file", type=["txt"])
    file2 = st.sidebar.file_uploader("Upload the second file", type=["txt"])

    if file1 and file2:
        st.sidebar.markdown("Files uploaded successfully!")
        st.subheader("Differences Between Files")

        # Read file contents
        file1_contents = read_file(file1)
        file2_contents = read_file(file2)

        # Display differences
        display_diff(file1_contents, file2_contents)

if __name__ == "__main__":
    main()
```

Save this script to a file, for example, `text_diff_visualizer.py`, and run it using the command:

```bash
streamlit run text_diff_visualizer.py
```

This script creates a Streamlit app with a sidebar where users can upload two text files. Once uploaded, it displays the differences between the two files using HTML for visualization, highlighting insertions and deletions.



# prompt_2

Not exactly how can you convert display_diff(file1_contents, file2_contents) into a csv file in panda make it the best way




# output_prompt_2

To convert the differences displayed by `display_diff(file1_contents, file2_contents)` into a CSV file using pandas, we need to extract the differences and organize them in a structured format before saving to a CSV file. We can modify the `display_diff()` function to return a DataFrame containing the differences. Then, we can use this DataFrame to save the differences to a CSV file. Here's how you can do it:

```python
import streamlit as st
import pandas as pd
from diff_match_patch import diff_match_patch

# Function to read the contents of a file
def read_file(uploaded_file):
    file_contents = ""
    try:
        file_contents = uploaded_file.getvalue().decode("utf-8")
    except AttributeError:
        st.error(f"File not uploaded.")
    return file_contents

# Function to compute differences and return a DataFrame
def compute_differences(file1_contents, file2_contents):
    dmp = diff_match_patch()
    diffs = dmp.diff_main(file1_contents, file2_contents)
    dmp.diff_cleanupSemantic(diffs)
    
    differences = []
    for diff in diffs:
        color = "Red" if diff[0] == -1 else "Green"
        differences.append((color, diff[1]))
    
    return pd.DataFrame(differences, columns=["Color", "Difference"])

# Streamlit app
def main():
    st.title("Text Difference Visualizer")

    # File upload
    st.sidebar.title("Upload Files")
    file1 = st.sidebar.file_uploader("Upload the first file", type=["txt"])
    file2 = st.sidebar.file_uploader("Upload the second file", type=["txt"])

    if file1 and file2:
        st.sidebar.markdown("Files uploaded successfully!")
        st.subheader("Differences Between Files")

        # Read file contents
        file1_contents = read_file(file1)
        file2_contents = read_file(file2)

        # Compute differences
        differences_df = compute_differences(file1_contents, file2_contents)
        
        # Display differences
        st.write(differences_df)

        # Save differences to CSV
        st.subheader("Save Differences to CSV")
        if st.button("Save Differences"):
            differences_df.to_csv("differences.csv", index=False)
            st.success("Differences saved successfully!")

if __name__ == "__main__":
    main()
```

In this script:

- The `compute_differences()` function computes the differences between the two files and organizes them into a DataFrame with columns "Color" and "Difference".
- The Streamlit app allows users to upload two text files, computes the differences between them, displays the differences in a DataFrame, and provides a button to save the differences to a CSV file named "differences.csv".
- When the "Save Differences" button is clicked, the differences are saved to the CSV file and a success message is displayed.

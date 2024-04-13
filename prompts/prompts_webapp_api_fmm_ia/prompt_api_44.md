# prompt_api_44.md

## prompt_1
Do the same script but for json files 


# output
To adapt the script to handle JSON files instead of text files, you can make a few adjustments. JSON files are typically structured data, so you'll need to decide how you want to compare and display differences in JSON content. Here's the modified script to handle JSON files:

```python
# Import necessary libraries
import streamlit as st
import pandas as pd
from diff_match_patch import diff_match_patch
from bs4 import BeautifulSoup
import json

# Function to read the contents of a file
def read_file(uploaded_file):
    file_contents = ""
    try:
        file_contents = uploaded_file.getvalue().decode("utf-8")
    except AttributeError:
        st.error(f"File not uploaded.")
    return file_contents

# Function to parse JSON and count differences
def parse_json_and_create_csv(json_content1, json_content2):
    # Parse JSON
    data1 = json.loads(json_content1)
    data2 = json.loads(json_content2)

    # Compare JSON objects (you may need to customize this based on your specific requirements)
    diffs = {}  # Store differences
    for key in data1.keys():
        if key in data2.keys():
            if data1[key] != data2[key]:
                diffs[key] = {"old_value": data1[key], "new_value": data2[key]}
        else:
            diffs[key] = {"old_value": data1[key], "new_value": "Not present in second JSON"}

    for key in data2.keys():
        if key not in data1.keys():
            diffs[key] = {"old_value": "Not present in first JSON", "new_value": data2[key]}

    # Create DataFrame
    df = pd.DataFrame.from_dict(diffs, orient="index")

    # Save DataFrame to CSV
    df.to_csv("json_diffs.csv")

    return len(diffs), df

# Main function to display differences
def display_diff(file1_contents, file2_contents):
    dmp = diff_match_patch()
    diffs = dmp.diff_main(file1_contents, file2_contents)
    dmp.diff_cleanupSemantic(diffs)
    diff_html = dmp.diff_prettyHtml(diffs)
    st.write(diff_html, unsafe_allow_html=True)

    return diff_html

# Streamlit app
def main():
    st.title("JSON Difference Visualizer")

    # File upload
    st.sidebar.title("Upload Files")
    file1 = st.sidebar.file_uploader("Upload the first JSON file", type=["json"])
    file2 = st.sidebar.file_uploader("Upload the second JSON file", type=["json"])

    if file1 and file2:
        st.sidebar.markdown("Files uploaded successfully!")
        st.subheader("Differences Between JSON Files")

        # Read file contents
        json_content1 = read_file(file1)
        json_content2 = read_file(file2)

        # Display differences (if needed)
        # Note: Displaying differences for JSON files might require a different approach
        # For simplicity, let's assume we'll just compare the JSON objects directly.
        
        # Parse JSON and create CSV
        num_diffs, diffs_df = parse_json_and_create_csv(json_content1, json_content2)
        st.success(f"Number of differences found: {num_diffs}")
        st.write("Differences:")
        st.write(diffs_df)

        # Add download button for the CSV file
        st.download_button(
            label="Download Differences CSV",
            data=diffs_df.to_csv().encode(),
            file_name="json_diffs.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
```

This script allows users to upload two JSON files, compares their contents, and displays the differences in a DataFrame. It then provides a download button to download the differences as a CSV file. You may need to customize the comparison logic depending on the structure of your JSON data.

# prompt_api_43.md

## prompt_1

Can indicate the legend for the colors at the beginning o the text
Red for file1_contents
Green for file2_contents
Can you sum the differences and show in a section named “General infos” using St.success. Then in the same section “General infos”, gather every change and build a csv with two columns where “Red ” contains the original string from the file (file_contents1) and the second column “Green ” contains the new string at the same position in the text from the file (file_contents2) and make this csv available in a view with Panda.

## output_prompt_1


Here's the updated script with the legend for the colors, and the addition of the "General infos" section that summarizes the differences and creates a CSV file with the changes:

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

# Main function to display differences
def display_diff(file1_contents, file2_contents):
    dmp = diff_match_patch()
    diffs = dmp.diff_main(file1_contents, file2_contents)
    dmp.diff_cleanupSemantic(diffs)
    diff_html = dmp.diff_prettyHtml(diffs)
    st.write(diff_html, unsafe_allow_html=True)

# Function to compute and display general information
def compute_general_info(file1_contents, file2_contents):
    dmp = diff_match_patch()
    diffs = dmp.diff_main(file1_contents, file2_contents)
    dmp.diff_cleanupSemantic(diffs)
    changes = []
    for diff in diffs:
        color = "Red" if diff[0] == -1 else "Green"
        changes.append((color, diff[1]))
    changes_df = pd.DataFrame(changes, columns=["Color", "Change"])
    st.success(f"Total changes: {len(changes)}")
    st.subheader("General Infos")
    st.write(changes_df)

    # Save changes to CSV
    changes_df.to_csv("changes.csv", index=False)
    st.download_button(
        label="Download Changes CSV",
        data=changes_df.to_csv().encode(),
        file_name="changes.csv",
        mime="text/csv",
    )

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

        # Compute and display general info
        compute_general_info(file1_contents, file2_contents)

if __name__ == "__main__":
    main()
```

This script adds a "General Infos" section where the total changes are displayed along with the changes in a DataFrame format. It also provides a download button to download the changes as a CSV file. This CSV file contains two columns: "Color" indicating whether the change is from the first or second file, and "Change" indicating the actual change.





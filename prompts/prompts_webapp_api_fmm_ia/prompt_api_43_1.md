# prompt_api_41.md

## prompt_1

As an advanced programmer in Python, with Streamlit, extend the script with a function that load "diff_html" and count the number of tag "ins" then grab the value between the tag "del" and rab the value between the tag "ins" and put in a cvs file with panda.

```html
<del style="background: rgb(255, 230, 230);">e monde</del>
<ins style="background: rgb(230, 255, 230);">'univers</ins>
```

```python
## output_1
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

# output

To extend the script with a function that loads "diff_html" and counts the number of "ins" tags, grabs the value between the "del" tags and "ins" tags, and puts them in a CSV file with pandas, you can follow these steps:

```python
# Import necessary libraries
import streamlit as st
import pandas as pd
from diff_match_patch import diff_match_patch
from bs4 import BeautifulSoup

# Function to read the contents of a file
def read_file(uploaded_file):
    file_contents = ""
    try:
        file_contents = uploaded_file.getvalue().decode("utf-8")
    except AttributeError:
        st.error(f"File not uploaded.")
    return file_contents


# Function to parse HTML and count 'ins' tags, and extract 'del' and 'ins' values
def parse_html_and_create_csv(diff_html):
    soup = BeautifulSoup(diff_html, "html.parser")
    ins_tags = soup.find_all("ins")
    del_tags = soup.find_all("del")

    # Count the number of 'ins' tags
    num_ins_tags = len(ins_tags)

    # Extract values between 'del' and 'ins' tags
    del_ins_values = []
    for del_tag, ins_tag in zip(del_tags, ins_tags):
        del_value = del_tag.get_text()
        ins_value = ins_tag.get_text()
        del_ins_values.append((del_value, ins_value))

    # Create a DataFrame
    data = {"Deleted": [pair[0] for pair in del_ins_values], "Inserted": [pair[1] for pair in del_ins_values]}
    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    df.to_csv("del_ins_values.csv", index=False)

    return num_ins_tags, df

# Main function to display differences
def display_diff(file1_contents, file2_contents):
    dmp = diff_match_patch()
    diffs = dmp.diff_main(file1_contents, file2_contents)
    dmp.diff_cleanupSemantic(diffs)
    diff_html = dmp.diff_prettyHtml(diffs)
    st.write(diff_html, unsafe_allow_html=True)

    return diff_html

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
        diff_html = display_diff(file1_contents, file2_contents)

        # Parse HTML and create CSV
        num_ins_tags, del_ins_df = parse_html_and_create_csv(diff_html)
        st.success(f"Number of 'ins' tags: {num_ins_tags}")
        st.write("Deleted and Inserted values:")
        st.write(del_ins_df)

        # Compute and display general info
        compute_general_info(file1_contents, file2_contents)

if __name__ == "__main__":
    main()
```

This script extends the existing Streamlit app to parse the HTML generated by the difference computation, count the number of "ins" tags, extract values between "del" and "ins" tags, and store them in a CSV file using pandas.

# prompt
Remove functions related to compute_general_info and add a download button for the function parse_html_and_create_csv


# output

To remove functions related to `compute_general_info` and add a download button for the function `parse_html_and_create_csv`, you can modify the Streamlit app as follows:

```python
# Import necessary libraries
import streamlit as st
import pandas as pd
from diff_match_patch import diff_match_patch
from bs4 import BeautifulSoup

# Function to read the contents of a file
def read_file(uploaded_file):
    file_contents = ""
    try:
        file_contents = uploaded_file.getvalue().decode("utf-8")
    except AttributeError:
        st.error(f"File not uploaded.")
    return file_contents

# Function to parse HTML and count 'ins' tags, and extract 'del' and 'ins' values
def parse_html_and_create_csv(diff_html):
    soup = BeautifulSoup(diff_html, "html.parser")
    ins_tags = soup.find_all("ins")
    del_tags = soup.find_all("del")

    # Count the number of 'ins' tags
    num_ins_tags = len(ins_tags)

    # Extract values between 'del' and 'ins' tags
    del_ins_values = []
    for del_tag, ins_tag in zip(del_tags, ins_tags):
        del_value = del_tag.get_text()
        ins_value = ins_tag.get_text()
        del_ins_values.append((del_value, ins_value))

    # Create a DataFrame
    data = {"Deleted": [pair[0] for pair in del_ins_values], "Inserted": [pair[1] for pair in del_ins_values]}
    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    df.to_csv("del_ins_values.csv", index=False)

    return num_ins_tags, df

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
        diff_html = display_diff(file1_contents, file2_contents)

        # Parse HTML and create CSV
        num_ins_tags, del_ins_df = parse_html_and_create_csv(diff_html)
        st.success(f"Number of 'ins' tags: {num_ins_tags}")
        st.write("Deleted and Inserted values:")
        st.write(del_ins_df)

        # Add download button for the CSV file
        st.download_button(
            label="Download Deleted and Inserted Values CSV",
            data=del_ins_df.to_csv().encode(),
            file_name="del_ins_values.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
```

This code will display the differences between the uploaded files, count the number of 'ins' tags, extract the values between 'del' and 'ins' tags, and display them. Additionally, it adds a download button for downloading the CSV file containing the deleted and inserted values.


# prompt

Whithout using the extra server through the command "python -m http.server 8000", how do you load an html named "003_html_player.html" containing the script and the json from a python made with Streamlit throught the command "streamlit run server.py". Write the file server.py with the proper command and a button named "View player" that serve in a new window or in iframe the "003_html_player.html"





# prompt_api_1.md

## prompt
As an advanced programmer in Python, with Streamlit, build in file named "ux.py" with two tabs "Save" and "Show". The first tab "Save" is  a form that post a text into the API named "LaylIA", connected to a SQLite database named "data/source.db". So, the webapp is saving the post inside the db. The second tab named "Show" show the records made into the database, if there is no records, show a message and if there is no db or table manage also the error.


## output

Here's an example of how you can create a Streamlit web application with two tabs, "Save" and "Show", where the "Save" tab allows users to post text to the "LaylIA" API connected to a SQLite database, and the "Show" tab displays records from the database or appropriate error messages:

```python
import streamlit as st
import requests
import sqlite3

# Function to interact with LaylIA API to save data
def save_to_laylia_api(content):
    try:
        response = requests.post("http://localhost:8000/write/", json={"content": content})
        if response.status_code == 200:
            st.success("Data saved successfully!")
        else:
            st.error("Failed to save data. Please try again.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Function to fetch records from the database
def fetch_records_from_db():
    try:
        conn = sqlite3.connect("data/source.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM post")
        records = cursor.fetchall()
        conn.close()
        return records
    except sqlite3.Error as e:
        st.error(f"SQLite error: {str(e)}")
        return []

# Streamlit UI
def main():
    st.title("LaylIA Database App")

    # Create tabs
    tabs = ["Save", "Show"]
    selected_tab = st.sidebar.selectbox("Select Tab", tabs)

    if selected_tab == "Save":
        st.subheader("Save Data to LaylIA")

        # Form to save data
        content = st.text_area("Enter your text here:")
        if st.button("Save"):
            if content.strip() != "":
                save_to_laylia_api(content)
            else:
                st.warning("Please enter some text to save.")

    elif selected_tab == "Show":
        st.subheader("Show Data from Database")

        # Fetch records from the database
        records = fetch_records_from_db()

        if not records:
            st.info("No records found in the database.")
        else:
            st.write("Records in the database:")
            for record in records:
                st.write(record)

if __name__ == "__main__":
    main()
```

In this code:

- We import the necessary libraries: Streamlit, requests, and sqlite3.
- We define two functions: `save_to_laylia_api()` to interact with the "LaylIA" API and save data, and `fetch_records_from_db()` to fetch records from the SQLite database.
- The `main()` function creates the Streamlit user interface with two tabs: "Save" and "Show".
- In the "Save" tab, users can enter text and save it to the "LaylIA" API using a form.
- In the "Show" tab, records from the database are displayed. If there are no records or if there is an error accessing the database, appropriate messages are displayed.
- Ensure that your "LaylIA" API is running on `http://localhost:8000/write/`, and you have a SQLite database named `source.db` in the `data` directory with a table named `post` already created.



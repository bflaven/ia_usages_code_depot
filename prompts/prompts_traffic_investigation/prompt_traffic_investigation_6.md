# prompt_traffic_investigation_6.md

## prompt_1
As an advanced programmer in Python, with Streamlit and other python librairies, can you write a script with a model that offer the best predcition for effective Tags using a csv file with the following columns "Date de publication","URL","Tags","Visites". Note that all the values are separated with semi-columns ";" and the values in "Tags" are coma separated.

```csv
"2024-01-08 17:08:25.000";"https://www.france24.com/fr/info-en-continu/20240108-🔴-remaniement-la-première-ministre-élisabeth-borne-démissionne";"France,Politique française,Emmanuel Macron,Élisabeth Borne,France,Gabriel Attal,FRANCE 24";"132181"
```

## output_1

Certainly! Below is a sample script that utilizes Streamlit along with other Python libraries such as pandas and scikit-learn to build a model for predicting effective tags based on the provided CSV file.

```python
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# Load the CSV data
@st.cache
def load_data(csv_file):
    df = pd.read_csv(csv_file)
    return df

# Preprocess the tags column
def preprocess_tags(tags):
    return tags.replace(',', ' ')

# Main function
def main():
    st.title("Effective Tags Prediction")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        st.write(data.head())

        # Preprocess tags
        data['Tags'] = data['Tags'].apply(preprocess_tags)

        # Split data into features and target
        X = data['Tags']
        y = data['Visites']

        # Vectorize the tags
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(X)

        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = MultinomialNB()
        model.fit(X_train, y_train)

        # Evaluate the model
        accuracy = model.score(X_test, y_test)
        st.write(f'Model Accuracy: {accuracy}')

        # Prediction
        tag_input = st.text_input("Enter tags separated by comma")
        if st.button("Predict"):
            tags = preprocess_tags(tag_input)
            tags_vectorized = vectorizer.transform([tags])
            prediction = model.predict(tags_vectorized)
            st.write(f'Predicted Visites: {prediction[0]}')

if __name__ == "__main__":
    main()
```

To run this script, make sure you have the necessary Python libraries installed:

```bash
pip install streamlit pandas scikit-learn
```

Save the script in a Python file, for instance, `tag_prediction_app.py`, and run it using Streamlit:

```bash
streamlit run tag_prediction_app.py
```

Once the Streamlit app is running, you can upload your CSV file, and the app will train a Multinomial Naive Bayes model on the provided data. You can then input tags separated by commas and get a prediction for the number of visits based on the model.

import streamlit as st
import pandas as pd

# Function to handle the conversion of non-string values to strings
def safe_replace(value, old_str, new_str):
    if isinstance(value, str):
        return value.replace(old_str, new_str)
    else:
        return value

def main():
    st.title("Tag Predictor")

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)

            # Preprocess data
            string_columns = ['Date de publication', 'URL', 'Tags']
            for column in string_columns:
                df[column] = df[column].apply(lambda x: safe_replace(x, ',', ';'))

            # Display the preprocessed data
            st.subheader("Preprocessed Data")
            st.write(df)

            # Your tag prediction model code goes here
            # You can implement your model and prediction logic based on the preprocessed data

            # Example: for demonstration purposes
            # st.subheader("Predicted Tags")
            # st.write(predicted_tags)

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


    

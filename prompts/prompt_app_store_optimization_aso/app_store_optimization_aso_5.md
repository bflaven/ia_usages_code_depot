
# app_store_optimization_aso_3.md

## prompt
As an advanced SEO, ASO expert and a seasoned developer in Streamlit and Python, add a submit button with primary class, when the user hits the button, print out all values that the user has selected.

Write, comment and leverage on the existing script. Do not improvise.

## ChatGPT
Certainly! I'll add a submit button with the primary class, and upon clicking it, the app will print out all the values that the user has entered or selected.

Here's the updated script:

```python
import streamlit as st

# Function to create a text input with a character limit and help text
def create_text_input(label, variable, char_limit, help_text):
    return st.text_input(
        label=f"{label} (Max {char_limit} characters)" if char_limit else label,
        max_chars=char_limit,
        key=variable,
        help=help_text
    )

# Function to create the language dropdowns
def create_language_dropdown(label, options, key):
    return st.selectbox(
        label=label,
        options=options,
        key=key
    )

# Function to print out all values
def print_values(values):
    for key, value in values.items():
        st.write(f"{key}: {value}")

# Main function to create the Streamlit app
def main():
    # Set the title of the Streamlit app
    st.title("SEO and ASO Prompt Generator")

    # Define variables for language options
    languages_rfi = ["EN", "CN", "ES", "KH", "BR", "PT", "RO", "RU", "SW", "VI", "FA"]
    languages_f24 = ["EN", "AR", "ES"]
    languages_mcd = ["EN", "FR"]

    # Create a radio button to select the Brand
    brand = st.radio(
        "Select Brand",
        ('rfi', 'f24', 'mcd'),
        index=0
    )

    # Based on the selected brand, set the appropriate languages
    if brand == 'rfi':
        selected_languages = languages_rfi
    elif brand == 'f24':
        selected_languages = languages_f24
    elif brand == 'mcd':
        selected_languages = languages_mcd

    # Create tabs for Android and IOS
    tab1, tab2 = st.tabs(["1. Tab ANDROID", "2. Tab IOS"])

    # Dictionary to hold all input values
    values = {}

    # Content for the Android tab
    with tab1:
        st.header("ANDROID")

        # Create text inputs for each variable
        values["aso_optimization_app_title"] = create_text_input("Title", "aso_optimization_app_title", 30, "Texte changé très rarement")
        values["aso_optimization_app_brief_description"] = create_text_input("Brief description", "aso_optimization_app_brief_description", 30, "Texte changé très rarement")
        values["aso_optimization_app_description"] = create_text_input("Description", "aso_optimization_app_description", 4000, "Texte changé très rarement")
        values["aso_optimization_app_new_marketing_text"] = create_text_input("New Marketing Text", "aso_optimization_app_new_marketing_text", None, "Texte changé à chaque publication")

        # Create language dropdown for the selected brand
        values["languages_android"] = create_language_dropdown("Languages", selected_languages, "languages_android")

    # Content for the IOS tab
    with tab2:
        st.header("IOS")

        # Create text inputs for each variable
        values["aso_optimization_app_title_ios"] = create_text_input("Title", "aso_optimization_app_title_ios", 30, "Texte changé très rarement")
        values["aso_optimization_app_subtitle"] = create_text_input("Subtitle", "aso_optimization_app_subtitle", 30, "Texte changé très rarement")
        values["aso_optimization_app_description_ios"] = create_text_input("Description", "aso_optimization_app_description_ios", 4000, "Texte changé très rarement")
        values["aso_optimization_app_promotional_text"] = create_text_input("Promotional Text", "aso_optimization_app_promotional_text", 170, "Texte changé très rarement")
        values["aso_optimization_app_new_marketing_text_ios"] = create_text_input("New Marketing Text", "aso_optimization_app_new_marketing_text_ios", 4000, "Texte changé à chaque publication")
        values["aso_optimization_app_keywords"] = create_text_input("Keywords", "aso_optimization_app_keywords", 170, "Texte changé très rarement")

        # Create language dropdown for the selected brand
        values["languages_ios"] = create_language_dropdown("Languages", selected_languages, "languages_ios")

    # Create a submit button with primary class
    if st.button("Submit", key="submit_button", type='primary'):
        print_values(values)

# Run the main function
if __name__ == "__main__":
    main()
```

### Explanation:
1. **Return Values from Input Functions:**
   - Modified `create_text_input` and `create_language_dropdown` functions to return the values of the inputs.

2. **Dictionary to Hold Input Values:**
   - Created a dictionary `values` to store all user inputs.

3. **Submit Button:**
   - Added a submit button with the primary class using `st.button("Submit", key="submit_button", type='primary')`.
   - When the button is clicked, the `print_values` function is called to print out all values stored in the `values` dictionary.

This script will now allow users to fill out the forms in each tab, select a brand, and upon submission, all entered and selected values will be printed to the Streamlit app interface.
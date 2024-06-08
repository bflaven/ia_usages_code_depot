"""
[env]
# Conda Environment
conda create --name fmm_fastapi_poc python=3.9.13
conda info --envs
source activate fmm_fastapi_poc
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n fmm_fastapi_poc

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manuel install
pip install mistralai
pip install langchain-mistralai
pip install python-dotenv
pip install streamlit-authenticator

# [path]
cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/prompt_app_store_optimization_aso

# LAUNCH the file
streamlit run 003_chatgpt_streamlit_app_store_optimization_aso.py

"""


import streamlit as st

# Function to create a text input with a character limit and help text
def create_text_input(label, variable, char_limit, help_text):
    return st.text_input(
        label=f"{label} (Max {char_limit} characters)" if char_limit else label,
        max_chars=char_limit,
        key=variable,
        help=help_text
    )

# Function to create a text area with a character limit and help text
def create_text_area(label, variable, char_limit, help_text):
    return st.text_area(
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

# Function to print out specific tab values
def print_tab_values(values, tab):
    st.write(f"Values for {tab} tab:")
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

    # Dictionary to hold all input values for each tab
    android_values = {}
    ios_values = {}


    # Content for the Android tab
    with tab1:
        st.session_state['tabs'] = "1. Tab ANDROID"  # Set the active tab
        st.header("ANDROID")

        # Create text inputs for each variable
        android_values["Title"] = create_text_input("Title", "aso_optimization_app_title_android", 30, "Texte changé très rarement")
        android_values["Brief description"] = create_text_input("Brief description", "aso_optimization_app_brief_description_android", 30, "Texte changé très rarement")
        android_values["Description"] = create_text_area("Description", "aso_optimization_app_description_android", 4000, "Texte changé très rarement")
        android_values["New Marketing Text"] = create_text_area("New Marketing Text", "aso_optimization_app_new_marketing_text_android", None, "Texte changé à chaque publication")

        # Create language dropdown for the selected brand
        android_values["Languages"] = create_language_dropdown("Languages", selected_languages, "languages_android")

    # Content for the IOS tab
    with tab2:
        st.session_state['tabs'] = "2. Tab IOS"  # Set the active tab
        st.header("IOS")

        # Create text inputs for each variable
        ios_values["Title"] = create_text_input("Title", "aso_optimization_app_title_ios", 30, "Texte changé très rarement")
        ios_values["Subtitle"] = create_text_input("Subtitle", "aso_optimization_app_subtitle", 30, "Texte changé très rarement")
        ios_values["Description"] = create_text_area("Description", "aso_optimization_app_description_ios", 4000, "Texte changé très rarement")
        ios_values["Promotional Text"] = create_text_input("Promotional Text", "aso_optimization_app_promotional_text", 170, "Texte changé très rarement")
        ios_values["New Marketing Text"] = create_text_area("New Marketing Text", "aso_optimization_app_new_marketing_text_ios", 4000, "Texte changé à chaque publication")
        ios_values["Keywords"] = create_text_input("Keywords", "aso_optimization_app_keywords", 170, "Texte changé très rarement")

        # Create language dropdown for the selected brand
        ios_values["Languages"] = create_language_dropdown("Languages", selected_languages, "languages_ios")

    # Create a submit button with primary class
    if st.button("Submit", key="submit_button", type='primary'):
        # Check which tab is selected and print the respective values
        if st.session_state['tabs'] == "1. Tab ANDROID":
            # print_tab_values(android_values, "ANDROID")
            st.write(android_values)
            
        elif st.session_state['tabs'] == "2. Tab IOS":
            # print_tab_values(ios_values, "IOS")
            st.write(ios_values)
            


# Run the main function
if __name__ == "__main__":
    main()



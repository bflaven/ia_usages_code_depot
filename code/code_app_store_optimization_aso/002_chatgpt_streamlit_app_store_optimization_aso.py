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
streamlit run 002_chatgpt_streamlit_app_store_optimization_aso.py

"""


import streamlit as st

# Function to create a text input with a character limit and help text
def create_text_input(label, variable, char_limit, help_text):
    st.text_input(
        label=f"{label} (Max {char_limit} characters)" if char_limit else label,
        max_chars=char_limit,
        key=variable,
        help=help_text
    )

# Function to create a text area with a character limit and help text
def create_text_area(label, variable, char_limit, help_text):
    st.text_area(
        label=f"{label} (Max {char_limit} characters)" if char_limit else label,
        max_chars=char_limit,
        key=variable,
        help=help_text
    )


# Function to create the language dropdowns
def create_language_dropdown(label, options, key):
    st.selectbox(
        label=label,
        options=options,
        key=key
    )

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

    # Content for the Android tab
    with tab1:
        st.header("ANDROID")

        # Create text inputs for each variable
        create_text_input("Title", "aso_optimization_app_title", 30, "Texte changé très rarement")
        create_text_input("Brief description", "aso_optimization_app_brief_description", 30, "Texte changé très rarement")
        create_text_input("Description", "aso_optimization_app_description", 4000, "Texte changé très rarement")
        create_text_input("New Marketing Text", "aso_optimization_app_new_marketing_text", None, "Texte changé à chaque publication")

        # Create language dropdown for the selected brand
        create_language_dropdown("Languages", selected_languages, "languages_android")

    # Content for the IOS tab
    with tab2:
        st.header("IOS")

        # Create text inputs for each variable
        create_text_input("Title", "aso_optimization_app_title_ios", 30, "Texte changé très rarement")
        create_text_input("Subtitle", "aso_optimization_app_subtitle", 30, "Texte changé très rarement")
        create_text_input("Description", "aso_optimization_app_description_ios", 4000, "Texte changé très rarement")
        create_text_input("Promotional Text", "aso_optimization_app_promotional_text", 170, "Texte changé très rarement")
        create_text_input("New Marketing Text", "aso_optimization_app_new_marketing_text_ios", 4000, "Texte changé à chaque publication")
        create_text_input("Keywords", "aso_optimization_app_keywords", 170, "Texte changé très rarement")

        # Create language dropdown for the selected brand
        create_language_dropdown("Languages", selected_languages, "languages_ios")

# Run the main function
if __name__ == "__main__":
    main()



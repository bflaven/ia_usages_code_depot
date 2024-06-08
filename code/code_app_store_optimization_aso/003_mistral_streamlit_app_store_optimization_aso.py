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
streamlit run 003_mistral_streamlit_app_store_optimization_aso.py

"""


import streamlit as st

# Define a function to create a form for a tab
def create_form(tab, variables, languages):
    with tab:
        st.write(f"Welcome to the ASO/SEO customization tab!")

        # Initialize session state with form values
        for var_info in variables.values():
            st.session_state[var_info["var"]] = ""
        for lang_name in languages.keys():
            st.session_state[lang_name] = ""

        # Create a form for the tab
        with st.form(f"{tab.title} form"):
            # Create a text area for each variable
            for var_name, var_info in variables.items():
                st.write(f"**{var_name}**")
                user_input = st.text_area(f"Enter your {var_name}", placeholder=f"Max {var_info['limit']} characters if applicable", key=var_info['var'])
                st.write(f"*Editorial update frequency: {var_info['freq']}*")

            # Create a dropdown for each language set
            for lang_name, lang_options in languages.items():
                st.write(f"**{lang_name}**")
                user_selection = st.selectbox("Select a language", [lang_opt.lower() for lang_opt in lang_options], key=lang_name)

            # Create a submit button and a reset button
            submit_button = st.form_submit_button("Submit")
            reset_button = st.button("Reset", key=f"{tab.title} reset")

            # If the reset button is clicked, clear the session state
            if reset_button:
                for var_info in variables.values():
                    st.session_state[var_info["var"]] = ""
                for lang_name in languages.keys():
                    st.session_state[lang_name] = ""

# Define variables and languages for Android
variables_android = {
    "title": {"var": "aso_optimization_app_title_android", "limit": 30, "freq": "Texte changé très rarement"},
    "brief_description": {"var": "aso_optimization_app_brief_description_android", "limit": 30, "freq": "Texte changé très rarement"},
    "description": {"var": "aso_optimization_app_description_android", "limit": 4000, "freq": "Texte changé très rarement"},
    "new_marketing_text": {"var": "aso_optimization_app_new_marketing_text_android", "limit": None, "freq": "Texte changé à chaque publication"}
}

languages_android = {
    "languages_rfi": ["EN", "CN", "ES", "KH", "BR", "PT", "RO", "RU", "SW", "VI", "FA"],
    "languages_f24": ["EN", "AR", "ES"],
    "languages_mcd": ["EN", "FR"]
}

# Define variables and languages for iOS
variables_ios = {
    "title": {"var": "aso_optimization_app_title_ios", "limit": 30, "freq": "Texte changé très rarement"},
    "subtitle": {"var": "aso_optimization_app_subtitle_ios", "limit": 30, "freq": "Texte changé très rarement"},
    "description": {"var": "aso_optimization_app_description_ios", "limit": 4000, "freq": "Texte changé très rarement"},
    "promotional_text": {"var": "aso_optimization_app_promotional_text_ios", "limit": 170, "freq": "Texte changé très rarement"},
    "new_marketing_text": {"var": "aso_optimization_app_new_marketing_text_ios", "limit": 4000, "freq": "Texte changé à chaque publication"},
    "keywords": {"var": "aso_optimization_app_keywords_ios", "limit": 170, "freq": "Texte changé très rarement"}
}

languages_ios = {
    "langues_rfi_fr": ["EN", "CN", "ES", "KH", "BR", "PT", "RO", "RU", "SW", "VI", "FA"],
    "langues_f24_fr": ["EN", "AR", "ES"],
    "langues_mcd_ar": ["EN", "FR"]
}

# Create tabs
tab1, tab2 = st.tabs(["1. Tab ANDROID", "2. Tab IOS"])

# Create a form for the Android tab
create_form(tab1, variables_android, languages_android)

# Create a form for the iOS tab
create_form(tab2, variables_ios, languages_ios)




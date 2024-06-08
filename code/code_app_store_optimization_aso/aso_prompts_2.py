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

# manual install
pip install python-dotenv
python -m pip install python-dotenv
conda install -c forge python-dotenv

pip install openai
python -m pip install openai
conda install -c forge openai


# [path]
cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/prompt_app_store_optimization_aso/

# launch the file
python aso_prompts_2.py

"""

# for api key
import os
from dotenv import load_dotenv

# Import the OpenAI class from the openai module
from openai import OpenAI

### 1. GET API KEY ###
# Load environment variables from the .env file
load_dotenv()

# Access the API key using os.getenv
api_key = os.getenv("OPENAI_API_KEY")

# Get the model
model_selected = "gpt-3.5-turbo"
# model_selected = "gpt-4-turbo"


### 2. GET STUFF FROM CHATGPOT ###
# Create an instance of the OpenAI class with the provided API key
client = OpenAI(api_key=api_key)

def openai_chat(prompt_key, user_input):
    # Create the user prompt from the dictionary
    user_prompt = aso_prompts[prompt_key].format(
        
        aso_app_main_language=aso_app_main_language,
        aso_app_main_os=aso_app_main_os,
        # aso_app_subtitle=aso_app_subtitle,
        aso_app_brand_name=aso_app_brand_name,
        # aso_blob_text=aso_blob_text,
        # aso_user_story=aso_user_story,
        # aso_app_main_language=aso_app_main_language,
        # aso_app_brand_name=aso_app_brand_name,
        # aso_app_primary_keywords=aso_app_primary_keywords,
    
        # keep it last
        user_input=user_input
        )

    # Create a chat completion using the OpenAI client
    response = client.chat.completions.create(
        model=model_selected, 
        messages=[{"role": "user", "content": user_prompt}]
    )

    # Response from the chat completion
    answer = response.choices[0].message.content

    # Assuming response and model_selected are defined and have valid values
    if model_selected == "gpt-3.5-turbo":
        input_price = response.usage.prompt_tokens * (0.46 / 1e6)
        output_price = response.usage.completion_tokens * (1.38 / 1e6)
    elif model_selected == "gpt-4-turbo":
        input_price = response.usage.prompt_tokens * (9.18 / 1e6)
        output_price = response.usage.completion_tokens * (27.55 / 1e6)
    else:
        raise ValueError("Invalid model selected. Please choose between 'gpt-3.5-turbo' and 'gpt-4-turbo'.")

    # Calculate the total price
    total_price = input_price + output_price

    # Return the answer, input price, output price, total price
    return {
        "answer": answer,
        "input_price": f"€ {input_price}",
        "output_price": f"€ {output_price}",
        "total_price": f"€ {total_price}"
    }


# keep it empty
# user_input = """
# """

###### All prompts ######

aso_prompts={

### 1. Title Optimization:

# "aso_title_optimization" : """ 
# As an ASO (App Store Optimization) expert proficient, could you create 10 compelling application titles in '{aso_app_main_language}' for an '{aso_app_main_os}' mobile application ? Please do follow these guidelines: 1. Keep the title within the 30-character limit to ensure it displays correctly across all devices. 2 Incorporate primary keywords that users are likely to search for '{aso_app_primary_keywords}' 3. Ensure your brand name '{aso_app_brand_name}'
# """,


### 2. Subtitle Optimization:
# "aso_subtitle_optimization" : """
# As an experienced ASO (App Store Optimization) specialist, please generate 10 engaging application subtitles in '{aso_app_main_language}' for a mobile app on '{aso_app_main_os}', incorporating '{aso_app_subtitle}'. To ensure diversity, use synonyms or variations of the primary keywords and include your brand name '{aso_app_brand_name}'. Please strictly adhere to the 30-character limit for subtitles to comply with the App Store guidelines.
# """,


### 3a. Keywords Extraction
# "aso_keywords_extraction" : """
# As an expert in SEO and ASO, please extract from the content below the top 50 keywords with the same language. List the keywords with in a comma-separeted list to ease the cut and paste like output format: ["keyword1", "keyword2", "keyword3"...]. The content is the following. Content: '{aso_blob_text}' as a reference. The keywords should be based on the most frequently used terms in the descriptions of the top three apps in this category.
# """,


### 3b. Keywords Extraction
# "aso_generate_keywords" : """
# Instruction: Generate the top 50 keywords for a mobile application.

# Background: The content is for a productivity app in the Business category. The target audience is busy professionals who need to manage their tasks and time effectively. The goal of the ASO strategy is to increase the visibility and the downloads of the app.

# Expectations:

# * List the keywords in a comma-separated format, like this: "keyword1, keyword2, keyword3".
# * Use lowercase letters and no punctuation, like this: "productivity" not "Productivity!"
# * Base the keywords on the most frequently used terms in the descriptions of the top three apps in this category.
# * Focus on the unique features and the benefits of the app, such as "task management", "time tracking", and "stress reduction".

# Output: ["keyword1", "keyword2", "keyword3"...]

# Note: Feel free to ask for clarification if needed, and let me know if you have any suggestions for improving the content or the keywords.
# """,

### 3. Add Keywords
# "aso_add_keywords" : """ 
# As an ASO (App Store Optimization) expert proficient, could you create a list of compelling application keywords for an '{aso_app_main_language}' mobile application ? Please do follow these guidelines: 1. Incorporate primary keywords that users are likely to search for '{aso_app_primary_keywords}' 3. Ensure your brand name '{aso_app_brand_name}'
# """,

### 4. Engaging App Descriptions
"aso_engaging_app_descriptions" : """ 
As an ASO (App Store Optimization) expert proficient, could you write a compelling application description in '{aso_app_main_language}' for an '{aso_app_main_os}' mobile application, using the following examples as a source of inspiration? Incorporate relevant keywords and ensure your brand name is '{aso_app_brand_name}'.

Here are the examples:

{user_input}

Please make sure to write a unique and engaging description that highlights the features and benefits of your app, while also incorporating the best practices and strategies from the examples provided.
""",

# ### 5. Create Keywords and Descriptions Clusters
# "aso_keywords_descriptions_clusters" : """
# As an advanced SEO and ASO expert, I would like you to analyze the following page from the Apple App Store and extract some key information for me.

# Page URL: {user_input}

# Category: Actualités

# Please provide me with the following:
# 1. A list of the 50 most commonly used keywords in this category.
# 2. The top 3 app descriptions in this category, based on their keyword usage, readability, and overall effectiveness.

# Your analysis and insights will be very helpful in optimizing our own app's presence in the App Store.
# """


}

### 1. Title Optimization:

# keep it empty
user_input = """
"""

# select prompt
# prompt_key = "aso_subtitle_optimization"

# variables
# aso_app_main_language = "FR"
# aso_app_main_os = "iOS"
# aso_app_primary_keywords = "actualité en direct, application France 24, contenus exclusifs, journalistes de France 24, articles, reportages, émissions, vidéos, français, anglais, espagnol, arabe, naviguer facilement, multimédias, partage sur les réseaux sociaux, info en continu, 24h/24 et 7j/7, faits-divers, grands événements internationaux, actualités françaises et internationales, rubriques spécialisées, Afrique, Moyen-Orient, Eco-Tech, Découvertes, replay vidéo, journaux sous-titrés, magazines de la rédaction, réseaux sociaux, Facebook, Twitter, Instagram, TikTok, YouTube, Telegram, Soundcloud, donnez-nous une note, laissez-nous un commentaire, France Médias Monde, Radio France Internationale, Monte Carlo Doualiya"
# aso_app_brand_name = "FRANCE 24"

# "FRANCE 24"
# user_input = "actualité en direct, application France 24, contenus exclusifs, journalistes de France 24, articles, reportages, émissions, vidéos, français, anglais, espagnol, arabe, naviguer facilement, multimédias, partage sur les réseaux sociaux, info en continu, 24h/24 et 7j/7, faits-divers, grands événements internationaux, actualités françaises et internationales, rubriques spécialisées, Afrique, Moyen-Orient, Eco-Tech, Découvertes, replay vidéo, journaux sous-titrés, magazines de la rédaction, réseaux sociaux, Facebook, Twitter, Instagram, TikTok, YouTube, Telegram, Soundcloud, donnez-nous une note, laissez-nous un commentaire, France Médias Monde, Radio France Internationale, Monte Carlo Doualiya"

### 2. Subtitle Optimization:

# prompt_key = "aso_subtitle_optimization"
# user_input = "FRANCE 24 - Info et actualités. Suivez l'actualité en direct et en continu en téléchargeant gratuitement l’application France 24."

# select prompt
# prompt_key = "aso_subtitle_optimization"
# 
# variables

# F24 iOS 
# aso_app_main_language = "FR"
# aso_app_main_os = "iOS"
# aso_app_subtitle = "FRANCE 24 - Info et actualités. Suivez l'actualité en direct et en continu en téléchargeant gratuitement l’application France 24."
# aso_app_brand_name = "FRANCE 24"

# RFI android 
# aso_app_main_language = "FR"
# aso_app_main_os = "ANDROID"
# aso_app_subtitle = "RFI - L'actualité mondiale. Articles, reportages, émissions, radio en direct et à la demande, alertes - tous les contenus de RFI sur l'actualité française, africaine et internationale à portée de main sur tous vos appareils."
# aso_app_brand_name = "RFI"

### 3a. Keywords Extraction
# prompt_key = "aso_keywords_extraction"

# aso_app_main_language = "FR"
# aso_keywords_source_url = "https://apps.apple.com/fr/charts/iphone/actualit%C3%A9s-apps/6009" 
# aso_keywords_category = "Actualités"

# aso_app_main_language = "FR"
# aso_keywords_source_url = "https://play.google.com/store/apps/category/NEWS_AND_MAGAZINES?hl=fr" 
# aso_keywords_category = "Actualités et magazines"


# aso_blob_text = """
# Google Actualités est un agrégateur qui organise et met en avant de façon personnalisée les informations du monde entier pour vous permettre de vous tenir rapidement aux courants des actualités et d'en savoir plus sur les sujets qui vous intéressent vraiment.


# Voici les différentes façons de suivre l'info avec Google Actualités :


# VOTRE SÉLECTION DU JOUR : il est presque impossible de suivre tous les sujets qui vous intéressent, mais grâce à votre sélection du jour, vous pourrez rester au fait des événements majeurs qui comptent pour vous. Recevez les principales actualités locales, nationales et internationales, mises à jour tout au long de la journée, ainsi que des actualités personnalisées selon vos centres d'intérêt.


# ACTUALITÉS LOCALES : suivez l'actualité de votre communauté grâce à des reportages et à des articles provenant de médias d'information locaux. Vous pouvez personnaliser et choisir plusieurs lieux, afin de savoir ce qui se passe autour de vous, où que vous soyez.


# COUVERTURE COMPLÈTE : explorez à fond un événement en découvrant plusieurs points de vue. La rubrique "Couverture complète" regroupe tout ce qui est accessible en ligne sur un sujet donné, mettant en avant son traitement par différents éditeurs et médias. D'un simple geste, découvrez le déroulement de l'événement qui vous intéresse et la façon dont les médias en parlent.


# ARTICLES RECOMMANDÉS : la rubrique "Pour vous" vous propose des actualités personnalisées liées à vos centres d'intérêt. Prenez le contrôle et personnalisez la sélection d'articles que vous recevez en suivant les sujets et les sources qui vous intéressent.


# ACCÈS DEPUIS N'IMPORTE QUEL APPAREIL : suivez l'actualité où que vous soyez. Associez l'application mobile Google Actualités au site Web news.google.com pour recevoir du contenu personnalisé sur tous vos appareils.


# Téléchargez gratuitement l'application CNEWS pour suivre toutes les actualités en France et dans le monde :

# - Suivez l’actualité en temps réel

# - Regardez la chaîne en direct

# - Recevez nos notifications pour ne manquer aucune info

# - Écoutez la chaîne en mode radio

# - Retrouvez vos émissions en replay et podcast


# Nouveautés :

# - "Le Monde" lance la version audio de ses articles.

# Nous franchissons ainsi une nouvelle étape dans notre ambition de s’adapter aux nouveaux usages. En voiture, dans le métro ou pendant un footing, l’information de qualité reste accessible.


# - Une seule application pour découvrir l'actualité en direct et l'intégralité du quotidien dès 11h, ainsi que les cahiers hebdomadaires, les suppléments mensuels et les hors séries.


# Cette application permet de retrouver facilement l’offre éditoriale du Monde :

# - la « Une » éditée par notre rédaction pour suivre les actualités

# - l’information en direct avec nos notifications, nos lives et notre fil « En continu »

# - l’intégralité des articles du Monde : nos reportages, enquêtes, tribunes, etc.

# - nos vidéos, infographies, photos et podcasts

# - « Découvrir » : un onglet vous permettant d'explorer l’actualité autrement ! Loisirs, vie quotidienne, récits, explications, etc.


# Nous avons mis en place différentes fonctionnalités afin d’améliorer vos expériences de lecture :

# - passez en mode « sombre » et modifiez la taille de la police pour optimiser votre confort de lecture

# - sélectionnez les articles que vous souhaitez lire plus tard

# - personnalisez vos rubriques pour accéder rapidement aux actualités qui vous intéressent


# Le Monde vous propose un traitement rigoureux, approfondi et fiable de l’information sur des thématiques variées :

# - l’actualité en France, en Europe et dans le monde

# - les dernières actualités à travers nos nombreuses rubriques : International, Planète, Politique, Société, Economie, etc.

# - mais aussi tous les grands événements sportifs, l’actualité scientifique, technologique, culturelle et artistique


# S’abonner au Monde, c’est soutenir une rédaction indépendante de 530 journalistes et pouvoir profiter des avantages suivants :

# - tous les contenus du  Monde en illimité, sur le site et l’application

# - écoutez la version audio des articles

# - le quotidien en version numérique dès 11 heures

# - l’application La Matinale, avec une édition tous les matins dès 7 heures

# - les archives depuis 1944
# """

### 3a. Keywords generation
# prompt_key = "aso_generate_keywords"

# aso_user_story = "The content is for a productivity app in the Business category. The target audience is busy professionals who need to manage their tasks and time effectively. The goal of the ASO strategy is to increase the visibility and the downloads of the app."

### 3. Add Keywords
# prompt_key = "aso_add_keywords"

# aso_app_main_language = "FR"
# aso_app_brand_name = "FRANCE 24"
# aso_app_primary_keywords = "News, Actualités, Information, Journal, Presse, Breaking, Live, Articles, Reportage, Politics, International, Economy, Finance, Culture, Sports, Weather, Local, Global, Headlines, Updates, Stories, Events, World, Media, Daily, Analysis, Insights, Highlights, Coverage, Alerts, Trending, Online, Mobile, Network, Bulletin, Update, Current, TV, Radio, Video, Stream, Reports, Digital, Read, Real-time, Data, Interactive, Subscription, In-depth, Highlights"

### 4. Engaging App Descriptions

prompt_key = "aso_engaging_app_descriptions"


aso_app_main_language = "FR"
aso_app_brand_name = "FRANCE 24"
aso_app_main_os = "iOS"

user_input = """
1. TF1 INFO - LCI: Actualités La Chaine Info
Découvrez toute l'actualité en direct avec TF1 INFO - LCI. Suivez les dernières nouvelles en France et à l'international, les reportages exclusifs, les analyses et les vidéos. Recevez des alertes pour rester informé en temps réel. L'info en continu, à portée de main.

2. Google Actualités
Google Actualités vous propose une couverture complète et personnalisée des actualités qui vous intéressent. Explorez les articles des plus grandes publications et recevez des alertes sur les sujets de votre choix. Restez informé grâce à des mises à jour en temps réel et à une sélection de sources fiables.

3. Le Monde, Live, Actu en direct
Retrouvez toute l'actualité avec Le Monde. Accédez à des articles en profondeur, des analyses, des vidéos et des photos. Suivez les événements en direct et recevez des notifications sur les sujets qui vous intéressent. Une couverture complète de l'actualité française et internationale, 24h/24.
"""


### 5. Create Keywords and Descriptions Clusters
# prompt_key = "aso_keywords_descriptions_clusters"
# user_input = """
# https://apps.apple.com/fr/charts/iphone/actualit%C3%A9s-apps/6009
# """

print('\n---- RESPONSE')
# Calling the function with the prompt key and user input
response = openai_chat(prompt_key, user_input)

# Print the response
print(response)


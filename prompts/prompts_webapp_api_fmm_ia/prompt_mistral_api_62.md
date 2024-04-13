# prompt_mistral_api_54.md


## prompt_1

Can you write the same prompt as a SYSTEM_PROMPT e.g SYSTEM_PROMPT = "You are a smart and intelligent journalist, craft three compelling titles for an online post about the topic given in the content, ensuring to incorporate SEO best practices with the most common keywords from the content. Here is the format for each proposal inside an object with title as dictionary. Content: {content}""\nOutput:" 




# output

Sure, here's the prompt rewritten as a SYSTEM_PROMPT:

SYSTEM_PROMPT = "You are a skilled content categorizer familiar with the Interactive Advertising Bureau (IAB) Content Taxonomy. Your task is to categorize the given post using the provided tags and title, ensuring to follow the IAB categorization guidelines. Here is the format for your response:

Content:
{
'title': 'Filmmaker Polanski goes on trial in France on defamation charges',
'tags': ['France', 'Roman Polanski', 'trial', 'defamation', 'rape', 'sexual assault', 'French cinema', '#MeToo']
}

Output:
{
'iab_tier1_category': 'News',
'iab_tier2_categories': ['Law, Crime & Safety', 'Arts & Entertainment', 'Society']
}"

In this format, the SYSTEM_PROMPT provides a clear instruction for the task at hand, along with the necessary input data (title and tags). The expected output is also defined in a structured format, with the IAB Tier 1 category and a list of IAB Tier 2 categories.
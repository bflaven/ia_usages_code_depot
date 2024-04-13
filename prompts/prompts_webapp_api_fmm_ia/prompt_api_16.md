# prompt_api_16.md

## prompt
As an advanced programmer in Python, with Streamlit, create a function that receive a json in a variable named "payload" and print each element in Streamlit page. For more inforation, here an example of the variable and the json structure given as example.
```json
payload = response.json()

{
  "src_lang": "fra_Latn",
  "tgt_lang": "eng_Latn",
  "input_text": "Selon une source policière, les faits se sont produits vers 13 h 15.",
  "output_text": [
    {
      "translation_text": "According to a police source, the incident occurred around 1:15 p.m."
    }
  ]
}
```


## output

```python
import streamlit as st

def display_payload(payload):
    st.write("Source Language:", payload["src_lang"])
    st.write("Target Language:", payload["tgt_lang"])
    st.write("Input Text:", payload["input_text"])
    
    st.write("Output Text:")
    for translation in payload["output_text"]:
        st.write("- Translation:", translation["translation_text"])

# Example JSON payload
payload = {
  "src_lang": "fra_Latn",
  "tgt_lang": "eng_Latn",
  "input_text": "Selon une source policière, les faits se sont produits vers 13 h 15.",
  "output_text": [
    {
      "translation_text": "According to a police source, the incident occurred around 1:15 p.m."
    }
  ]
}

# Display the payload using Streamlit
st.title("JSON Payload Display")
display_payload(payload)
```
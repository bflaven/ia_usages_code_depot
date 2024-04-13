# prompt_api_7.md

## prompt
As an advanced programmer in Python, with Streamlit, show the errors in original_text in red with st.warning with the error text inside and show the corrected_text in green with st.success with the error text inside. Here some other info: spelling_data['errors_detected']  is the index number for error, spelling_data['corrections'] where spelling_data['corrections'][0] is the wrong stuff load in st.warning , spelling_data['corrections'][0] is good stuff in st.success.
Here is an complete example with data of spelling_data['corrections']

[
  [
    "vission",
    "vision"
  ],
  [
    " ,",
    ","
  ],
  [
    "Frannçois",
    "François"
  ],
  [
    "Badinter",
    "Badiner"
  ],
  [
    "ait",
    "est"
  ],
  [
    "nnuit",
    "nuit"
  ]
]

## output


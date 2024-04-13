# prompt_api_4.md

## prompt
As an advanced programmer in Python, with FastAPI, write a endpoint named "spelling" that will launch a file named "spellchecker.py" including the code below but with the text posted via the endpoint. When the script is done, send back to the endpoint named "spelling" the values computed by the script on the text sent into the following variables: original_text, corrected_text, errors_detected, corrections.

The code has text given in french as example but it has to be tranformed as a variable for the function. Here the code below:

tool = language_tool_python.LanguageTool('fr-FR')

# La vision intangible, universelle, des droits de l’homme que portait le garde des sceaux de François Mitterrand a imprégné jusqu’au bout ses écrits et prises de position. Robert Badiner est mort, dans la nuit du 8 au 9 février, à l’age de 95 ans.

text = 'La vission intangible , universelle, des droits de l’homme que portait le garde des sceaux de Frannçois Mitterrand a imprégné jusqu’au bout ses écrits et prises de position. Robert Badinter ait mort, dans la nnuit du 8 au 9 février, à l’age de 95 ans.'

matches = tool.check(text)
result = len(matches)
print('\n--- errors detected')
print(result)
# print('\n--- errors detailed')
# print(matches)

my_mistakes = []
my_corrections = []
start_positions = []
end_positions = []
 
for rules in matches:
    if len(rules.replacements)>0:
        start_positions.append(rules.offset)
        end_positions.append(rules.errorLength+rules.offset)
        my_mistakes.append(text[rules.offset:rules.errorLength+rules.offset])
        my_corrections.append(rules.replacements[0])

print('\n--- result for corrections made')
corrections = list(zip(my_mistakes,my_corrections))
print(corrections)



corrected_text = tool.correct(text)
print('\n--- corrected_text')
print(corrected_text)
tool.close()



## output

To create a FastAPI endpoint named "spelling" that accepts text input and launches the "spellchecker.py" script to compute values based on the provided text, you can follow the example below:

First, create the FastAPI endpoint:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/spelling")
def run_spellchecker(text_request: TextRequest):
    # Create a temporary file to store the provided text
    temp_file_path = "temp_text.txt"
    with open(temp_file_path, "w") as temp_file:
        temp_file.write(text_request.text)

    # Run the spellchecker.py script with the provided text file
    process = subprocess.Popen(['python', 'spellchecker.py', temp_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Remove the temporary file
    subprocess.run(["rm", temp_file_path])

    # Decode the output from bytes to string
    output_str = output.decode('utf-8')

    # Parse the output which is in JSON format
    try:
        spellcheck_result = json.loads(output_str)
        return spellcheck_result
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding spellchecker output")
```

Make sure that your FastAPI server and the "spellchecker.py" script are in the same directory for this code to work properly.

And here is the modified "spellchecker.py" script:

```python
import sys
import json
import language_tool_python

# Ensure the correct number of command-line arguments
if len(sys.argv) != 2:
    print("Usage: python spellchecker.py <input_file>")
    sys.exit(1)

# Load the language tool
tool = language_tool_python.LanguageTool('fr-FR')

# Read the text from the input file
input_file = sys.argv[1]
with open(input_file, "r") as file:
    text = file.read()

# Perform spell checking
matches = tool.check(text)
result = len(matches)

my_mistakes = []
my_corrections = []
start_positions = []
end_positions = []

for rules in matches:
    if len(rules.replacements) > 0:
        start_positions.append(rules.offset)
        end_positions.append(rules.errorLength + rules.offset)
        my_mistakes.append(text[rules.offset : rules.errorLength + rules.offset])
        my_corrections.append(rules.replacements[0])

corrections = list(zip(my_mistakes, my_corrections))

corrected_text = tool.correct(text)

# Prepare the result dictionary
result_dict = {
    "original_text": text,
    "corrected_text": corrected_text,
    "errors_detected": result,
    "corrections": corrections
}

# Output the result as JSON
print(json.dumps(result_dict))

tool.close()
```

This script reads the input text from a file specified as a command-line argument. The FastAPI endpoint receives the text through a POST request and passes it to the spellchecker script. Finally, it returns the computed values back to the client.
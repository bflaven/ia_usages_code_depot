# prompt_api_4.md

## prompt
As an advanced programmer in Python, with FastAPI, write a endpoint named "spelling" that contain the logic below. The field "text" is the value that will be posted into the endpoint named "spelling".

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

from fastapi import FastAPI, HTTPException

# for Spelling
from pydantic import BaseModel
import language_tool_python

app = FastAPI()

# for Spelling
class TextRequest(BaseModel):
    text: str

@app.post("/spelling")
async def spelling(text_request: TextRequest):
    tool = language_tool_python.LanguageTool('fr-FR')

    text = text_request.text
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
            my_mistakes.append(text[rules.offset:rules.errorLength + rules.offset])
            my_corrections.append(rules.replacements[0])

    corrections = list(zip(my_mistakes, my_corrections))

    corrected_text = tool.correct(text)
    tool.close()

    return {
        "original_text": text,
        "corrected_text": corrected_text,
        "errors_detected": result,
        "corrections": corrections
    }

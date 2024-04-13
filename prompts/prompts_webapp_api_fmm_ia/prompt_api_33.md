# prompt_api_33.md

## prompt
As an advanced programmer in Python create a function that receive from an endpoint named "ollama-generate" a json like the one below illustrated in "response" then parse and fetch the values "Title" and "Keywords" for each proposal from the "response"

```json
"response": " \"proposal_1\": {\"Title\": \"China Urges Israel to Halt Military Operation in Gaza's Rafah, Calls for Immediate Ceasefire\", \"Keywords\": [\"Israel\", \"Gaza\", \"Rafah\", \"military operation\", \"ceasefire\", \"China\"]},\n\"proposal_2\": {\"Title\": \"Calls for Immediate Ceasefire in Gaza as China Condemns Israel's Military Operation\", \"Keywords\": [\"Gaza\", \"Israel\", \"military operation\", \"ceasefire\", \"China\", \"humanitarian crisis\"]},\n\"proposal_3\": {\"Title\": \"King Abdallah II Advocates for Immediate Ceasefire in Gaza at White House Meeting with Biden\", \"Keywords\": [\"Gaza\", \"Israel\", \"ceasefire\", \"Joe Biden\", \"King Abdallah II\", \"otages\"]}",
```

## output


To achieve this task, we'll create a Python function that fetches the "Title" and "Keywords" for each proposal from the given JSON response. Here's how you can implement the function:

```python
import json
import requests

def fetch_proposals(endpoint_url):
    try:
        # Fetch the JSON response from the endpoint
        response = requests.get(endpoint_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Extract the JSON data from the response
        data = response.json()

        # Parse and fetch the values "Title" and "Keywords" for each proposal
        proposals = {}
        for proposal, details in data.items():
            title = details["Title"]
            keywords = details["Keywords"]
            proposals[proposal] = {"Title": title, "Keywords": keywords}

        return proposals

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {endpoint_url}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None

# Example usage:
endpoint_url = "http://example.com/ollama-generate"  # Replace with your endpoint URL
proposals = fetch_proposals(endpoint_url)
if proposals:
    for proposal, details in proposals.items():
        print(f"Proposal: {proposal}")
        print(f"Title: {details['Title']}")
        print(f"Keywords: {details['Keywords']}")
        print()
```

Here's a breakdown of the function:

1. It defines a function `fetch_proposals` that takes an endpoint URL as input.
2. It makes a GET request to the specified endpoint to fetch the JSON response.
3. It extracts the JSON data from the response and parses it.
4. It iterates through each proposal in the JSON data, extracting the "Title" and "Keywords" for each proposal.
5. It returns a dictionary containing the proposals along with their titles and keywords.
6. It handles exceptions such as HTTP errors and JSON decoding errors.

You can replace `"http://example.com/ollama-generate"` with the actual endpoint URL from which you want to fetch the data. The function returns a dictionary with the proposals, titles, and keywords, which you can then process or use as needed.
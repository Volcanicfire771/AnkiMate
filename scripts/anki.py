import json
import requests
import urllib.request


# AnkiConnect API URL
ANKI_CONNECT_URL = "http://localhost:8765"

# Function to add a flashcard
def add_flashcard(deck_name, question, answer):
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": "Basic",
                "fields": {
                    "Front": question,
                    "Back": answer
                },
                "tags": ["pdf_import"],
                "options": {
                    "allowDuplicate": False
                }
            }
        }
    }

    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    
    if "error" in result and result["error"] is not None:
        print(f"Error adding card: {result['error']}")
    else:
        print(f"Card added successfully: {result}")

# Example Usage
deck_name = "Ahmed_Mohsen"  # Change to your desired deck
question = "What is the capital of France?"
answer = "Paris"

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']




invoke('createDeck', deck=deck_name)

add_flashcard(deck_name, question, answer)
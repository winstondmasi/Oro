import requests  # type: ignore
import json

from extract_youtube import *
from bert_summarizer import *
from question_generator import *

# make request to ankiConnect
def anki_request(action, **params):
    request_data = json.dumps({
        "action" : action,
        "versions": 6,
        "params": params
    })

    response = requests.post("http://localhost:8765", data=request_data)
    response_data = response.json()

    if len(response_data) > 2:
        raise Exception("Unexecptected Number of Fields")
    if "result" not in response_data:
        raise Exception("Mising result tag in field required in response")
    return response_data['result']

# add questions to deck
def add_notes_to_anki(deck_name, front, back):
    notes = {
        "deckName": deck_name,
        "modelName": "Basic",
        "fields":{
            "Front": front,
            "Back": back
        },
        "tags":[],
        "options":{
            "allowDuplicate": False
        }
    }
    
    return anki_request("addNote", notes)

# process transcript to generate content for flashcards
def create_flashcards(video_id):
    deck_nam = "Default" 

    generate = generate_questions_from_summary(video_id)

    # loop through generated questions to create multiple flashcards 
    for qa_pair in generate:
        front = qa_pair['question']
        back = qa_pair['answer']
        add_notes_to_anki(deck_nam, front, back)

    print("Added Notes: ", len(generate))
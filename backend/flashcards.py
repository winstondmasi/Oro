import genanki 

from extract_youtube import *
from bert_summarizer import *
from question_generator import *



# create anki model
def create_model(model_id, model_name):

    return genanki.Model(
        model_id,
        model_name,
        fields=[
            {'name' : 'question'},
            {'name' : 'answer'},
        ],
        template=[
            {
                'name':'Card 1',
                'qfmt': '{{question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{answer}}'
            }
        ])
    

# create anki deck
def create_deck(deck_id, deck_name):
    return genanki.Deck(
        deck_id,
        deck_name
    )

# add cards to anki
def add_cards_to_anki(deck, model, cards):

    for question, answer in cards:
        note = genanki.Note(
            model=model,
            fields=[question, answer]
        )
        deck.add_note(note)

# writes the anki deck to apkg file
def write_deck_to_file(deck, output_file):
    package = genanki.Package(deck)
    package.write_to_file(output_file)

# put all the small functions together to create apkg file for anki
def create_apkg(deck_name, model_name, cards, output_file):
    model_id = 1607392319
    deck_id = 2059400110

    model = create_model(model_id, model_name)
    deck = create_deck(deck_id, deck_name)
    add_cards_to_anki(deck, model, cards)
    write_deck_to_file(deck, output_file)


'''
Example Call
deck_name = "test"
model_name = "test"
cards = [
    ("What is the capital of France?", "Paris"),
    ("What is 2 + 2?", "4"),
    ("Who wrote 'To Kill a Mockingbird'?", "Harper Lee")
]
output_file = "test.apkg"
create_apkg(deck_name, model_name, cards, output_file)
'''
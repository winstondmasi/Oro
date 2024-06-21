import unittest

from unittest.mock import patch, MagicMock

from extract_youtube import fetch_transcript
from bert_summarizer import *
from question_generator import *
from flashcards import create_apkg, add_cards_to_anki

from flask import jsonify
from app import app

class TestExtractYTSummarizer(unittest.TestCase):

    @patch('extract_youtube.YouTubeTranscriptApi.get_transcript')
    def test_fetch_transcript(self, mock_get_transcript):
        # mock return value of get_transcript
        mock_transcript = [
            {'text': 'Hey there', 'start': 7.58, 'duration': 6.13},
            {'text': 'how are you', 'start': 14.08, 'duration': 7.58}
        ]
        mock_get_transcript.return_value = mock_transcript

        # call instance of get_transcripts
        video_id = 'video123'
        results = fetch_transcript(video_id)

        # assert functions returns the expected results 
        self.assertEqual(results, mock_transcript)
        mock_get_transcript.assert_called_once_with(video_id)

    
    
    @patch('extract_youtube.YouTubeTranscriptApi.get_transcript')
    def test_clean_transcript(self, mock_get_transcript):
        # mock return value of get_transcript
        mock_transcript = [{'text': 'hello', 'start': 1.0, 'duration': 2.0}, {'text': 'world', 'start': 3.0, 'duration': 4.0}]
        mock_get_transcript.return_value = mock_transcript

        expected_text = 'hello world'

        # call instance of get_transcripts
        cleaned_text = clean_transcript(mock_transcript)

        # check to see that the results of the clean_transcript function are that of a string
        self.assertEqual(cleaned_text, expected_text)

class TestBertSummarizer(unittest.TestCase):

    @patch('bert_summarizer.summarize_text')
    def test_summarize_text(self, mock_input):

        example_text = '''
        The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price.
        The deal, first reported by The Real Deal, was for $150 million, according to a source familiar with the deal.
        Mubadala, an Abu Dhabi investment fund, purchased 90% of the building for $800 million in 2008.
        Real estate firm Tishman Speyer had owned the other 10%.
        The buyer is RFR Holding, a New York real estate company.
        Officials with Tishman and RFR did not immediately respond to a request for comments.
        It's unclear when the deal will close.
        The building sold fairly quickly after being publicly placed on the market only two months ago.
        The sale was handled by CBRE Group.
        '''
        mock_input.return_value = example_text

        result = summarize_text(example_text)
        self.assertGreaterEqual(len(result), 40)
        self.assertIsInstance(result, str)

class TestQuestionGeneration(unittest.TestCase):

    @patch('question_generator.pipeline')
    def test_question_generation(self, mock_pipleline):
        mock_nlp = MagicMock()
        mock_pipleline.return_value = mock_nlp

        #mock return value for generate_questions
        mock_nlp.return_value = [{'answer': '42', 'question': 'What is the answer to life, the universe, and everything?'}]

        text = "What is the answer to life, the universe, and everything? The answer is 42."
        questions_generated = generate_questions(text)

        self.assertEqual(questions_generated, mock_nlp.return_value)
        mock_nlp.assert_called_once_with(text)

    def test_multiple_key_value_pairs(self):
        data = [{'answer': '42', 'question': 'What is the answer to life, the universe and everything?'}]
        result = dict_to_tuple(data)
        self.assertEqual(result, [('What is the answer to life, the universe and everything?', '42')])

class TestFlashCards(unittest.TestCase):

    def test_add_cards_to_anki(self):
        deck = MagicMock()
        model = MagicMock()
        cards = [('question1', 'answer1'), 
                 ('question2', 'answer2')]

        add_cards_to_anki(deck, model, cards)

        self.assertEqual(deck.add_note.call_count, 2)

        note1 = deck.add_note.call_args_list[0][0][0]
        self.assertEqual(note1.model, model)
        self.assertEqual(note1.fields, ['question1', 'answer1'])

        note2 = deck.add_note.call_args_list[1][0][0]
        self.assertEqual(note2.model, model)
        self.assertEqual(note2.fields, ['question2', 'answer2'])
    
    
    @patch('flashcards.write_deck_to_file')
    @patch('flashcards.add_cards_to_anki')
    @patch('flashcards.create_deck')
    @patch('flashcards.create_model')
    def test_create_apkg(self, mock_create_model, mock_create_deck, mock_add_cards_to_anki, mock_write_deck_to_file):
        # set up mock objects
        mock_model_name = "test_model"
        mock_deck_name = "test_deck"
        mock_cards = [
            ("What is the capital of France?", "Paris"),
            ("What is 2 + 2?", "4"),
            ("Who wrote 'To Kill a Mockingbird'?", "Harper Lee")
        ]
        mock_package = 'test_package.apkg'

        mock_model = MagicMock()
        mock_deck = MagicMock()
        
        mock_create_model.return_value = mock_model
        mock_create_deck.return_value = mock_deck

        create_apkg(mock_deck_name, mock_model_name, mock_cards, mock_package)

        mock_create_model.assert_called_once_with(1607392319, mock_model_name)
        mock_create_deck.assert_called_once_with(2059400110, mock_deck_name)
        mock_add_cards_to_anki.assert_called_once_with(mock_deck, mock_model, mock_cards)
        mock_write_deck_to_file.assert_called_once_with(mock_deck, mock_package)


class TestFlaskGetSummaryOrFlashcards(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    
    @patch('app.summarize_transcript')
    def test_get_summary(self, mock_summarize_transcript):
        mock_summarize_transcript.return_value = "summary"
        response = self.app.post('/backend/video_id', json = {'video_id': 'video123', 'request_type': 'summary'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"Summary: {mock_summarize_transcript.return_value}", response.get_data(as_text=True))

    
    @patch('app.generate_questions_from_summary')
    def test_get_flashcards(self, mock_created_apkg):
        mock_created_apkg.return_value = "flashcards.apkg"

        response = self.app.post('/backend/video_id', json = {'video_id': 'video123', 'request_type': 'flashcards'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"flashcards.apkg", response.data)
        self.assertEqual(mock_created_apkg.call_count, 1)
    
if __name__ == '__main__':
    unittest.main()
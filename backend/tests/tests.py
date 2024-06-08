import unittest
from unittest.mock import patch
from extract_youtube import *
from bert_summarizer import *

class TestExtractYTSummarizer(unittest.TestCase):


    def example_transscript(self):
        list_of_dicts = [
            {
                'text': 'Hey there',
                'start': 7.58,
                'duration': 6.13
            },
            {
                'text': 'how are you',
                'start': 14.08,
                'duration': 7.58
            }
        ]

        return list_of_dicts

    @patch('extract_youtube.YouTubeTransccriptAPI')
    def test_fetch_transcript(self):

        # example url (click it for a surprise lol!)
        mock_video_id = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"


        # check to see if fetch_transcript results in an instance of a list
        get_transctipts = fetch_transcript(mock_video_id)
        self.assertIsInstance(get_transctipts, list)

        # example list call
        example_list = TestExtractYTSummarizer.example_transscript()

        # check that each item in the list is a dictionary as well as expected keys
        expected_keys = ['text', 'start', 'duration']

        for dictionary in example_list:

            self.assertIsInstance(dictionary, dict)

            for key, value in dictionary.items():

                self.assertIsInstance(key, expected_keys)

                if key == 'start' or key == 'duration':
                    self.assertIsInstance(value, int)
                else:
                    self.assertIsInstance(value, str)

        


    @patch('extract_youtube.YouTubeTransccriptAPI')
    def test_clean_transcript(self):
        # call instance of get_transcripts
        mock_video_id = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
        get_transctipts = fetch_transcript(mock_video_id)

        # check to see that the results of the clean_transcript function are that of a string
        results = clean_transcript(get_transctipts)
        self.assertIsInstance(results, str)


class TestBertSummarizer(unittest.TestCase):

    @patch('bert_summarizer.Summarizer')
    def test_summarize_text(self):

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

        result = summarize_text(example_text)
        self.assertIsInstance(result, str)

        if len(example_text) > 600:
            self.assertGreaterEqual(len(result), 40)

class TestQuestionGeneration(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
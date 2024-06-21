from flask import Flask, render_template, request, send_file, url_for, jsonify
from flask_cors import CORS 

from bert_summarizer import *
from flashcards import *

import traceback

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/backend/video_id', methods=['POST'])
def get_summary_or_flashcards():
    """
    Endpoint for retrieving a summary of a video by its ID.

    This endpoint expects a JSON payload with a 'video_id' field in the request body.
    It calls the 'summarize_transcript' function with the received video ID to generate a summary.
    The summary is then returned as a JSON response with a 'response' field.

    Returns:
        A JSON response containing the summary of the video.

    Example:
        POST /backend/video_id
        {
            "video_id": "VIDEO_ID"
        }
        Response:
        {
            "response": "SUMMARY"
        }

    Retrieves flashcards based on a video ID received in a POST request.
    Calls 'generate_questions_from_summary' to generate questions from the summary of the video.
    Creates an Anki package (apkg) with the generated flashcards.
    
    Returns:
        The Anki package (apkg) containing the flashcards.
    """
    video_id = request.json
    received_video_id = video_id.get('video_id', '')

    request_type = video_id.get('request_type', '')

    if request_type == 'flashcards':
        dict_cards = generate_questions_from_summary(received_video_id)

        tuple_cards = dict_to_tuple(dict_cards)

        flashcards = create_apkg('Deck', 'Summary', tuple_cards, 'flashcards.apkg')

        return send_file(flashcards, as_attachment=True,download_name='flashcards.apkg') 
    if request_type == 'summary':
        result = summarize_transcript(received_video_id)

        return jsonify(response=f"Summary: {result}")

'''
@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error), exc_info=True)
    traceback.print_exc()
'''

if __name__ == '__main__':
    app.run(debug=True)




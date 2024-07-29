from flask import Flask, request, send_file, send_from_directory, jsonify
from flask_cors import CORS 

from backend.bert_summarizer import *
from backend.flashcards import *
from backend.question_generator import generate_questions_from_summary, dict_to_tuple

import traceback

app = Flask(__name__, static_folder='../frontend/build')
CORS(app)

# Serve the index.html file
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

# Serve static files
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/backend/video_id', methods=['POST'])
def get_summary_or_flashcards():
    """
    Endpoint for retrieving a summary of a video by its ID or generating flashcards.

    This endpoint expects a JSON payload with a 'video_id' and 'request_type' field in the request body.
    'request_type' can be either 'summary' or 'flashcards'.

    Returns:
        A JSON response containing the summary of the video or an Anki package (apkg) with flashcards.
    """
    video_id = request.json.get('video_id', '')
    request_type = request.json.get('request_type', '')

    if not video_id:
        return jsonify(error="Missing 'video_id' field in request body"), 400
    
    if not request_type:
        return jsonify(error="Missing 'request_type' field in request body"), 400

    try:
        if request_type == 'flashcards':

            dict_cards = generate_questions_from_summary(video_id)

            tuple_cards = dict_to_tuple(dict_cards)

            flashcards_path = create_apkg('Deck', 'Summary', tuple_cards, 'flashcards.apkg')

            if flashcards_path and os.path.exists(flashcards_path):
                return send_file(flashcards_path, as_attachment=True,download_name='flashcards.apkg') 
            else:
                return jsonify(error="Failed to create flashcards"), 500
        
        elif request_type == 'summary':

            result = summarize_transcript(video_id)

            return jsonify(response=f"Summary: {result}")
        
        else:

            return jsonify(error="Invalid 'request_type' field in request body"), 400
        
    except Exception as e:
        app.logger.error('Error processing request: %s', str(e), exc_info=True)

        traceback.print_exc()

        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error), exc_info=True)
    traceback.print_exc()
    return jsonify(error="Internal Server Error"), 500


if __name__ == '__main__':
    app.run(debug=True)
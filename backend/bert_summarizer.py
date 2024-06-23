from summarizer import Summarizer 
from extract_youtube import *

# summarize text using bert
def summarize_text(input):

    model = Summarizer()

    if input is not None and len(input) > 600:
        result = model(input, min_length = 40)
        full = ''.join(result)
        return full
    
    elif input is not None and len(input) < 600:
        result = model(input)
        full = ''.join(result)
        return full

    else:
        return None
    
# fetch, clean and summarize yt transcripts in one go
def summarize_transcript( video_id):

    clean_text = fetch_and_clean_transcript(video_id)
    return summarize_text(clean_text)
from summarizer import Summarizer 
from extract_youtube import *

# summarize text using bert
def summarize_text(input):

    model = Summarizer()

    if len(input) > 600:
        result = model(input, min_lenght = 40)
        return result
    
    return model(input)

# fetch, clean and summarize yt transcripts in one go
def summarize_transcript(self, video_id):

    clean_text = fetch_and_clean_transcript(video_id)
    return summarize_text(clean_text)
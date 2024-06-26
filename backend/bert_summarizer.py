from summarizer import Summarizer 
from backend.extract_youtube import *

# summarize text using bert
def summarize_text(input):
    print(f"Input length for text summary is = {len(input)}")
    model = Summarizer()

    if input is not None and len(input) > 3000 and len(input) < 9000:
        #result = model(input, ratio=0.4)
        result = model(input, num_sentences=7)
        full = ''.join(result)
        return full
    
    elif input is not None and len(input) < 600:
        result = model(input)
        full = ''.join(result)
        return full

    else:
        print(f"Input is none or empty")
        return None
    
# fetch, clean and summarize yt transcripts in one go
def summarize_transcript( video_id):
    print(f"Fetching transcript for video id = {video_id}")
    clean_text = fetch_and_clean_transcript(video_id)
    print(f"Cleaned Transcript first 10 character is : {clean_text[0:10]}")
    summary = summarize_text(clean_text)
    print(f"Summary: {summary}")
    return summary
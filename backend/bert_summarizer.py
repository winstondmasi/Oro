from summarizer import Summarizer 
from backend.extract_youtube import *

# summarize text using bert
def summarize_text(input):
    print(f"Input length for text summary is = {len(input)}")
    model = Summarizer()

    result = model(input, ratio=0.3)
    full = ''.join(result)
    print(f"The result is: {full}")
    return full
    
# fetch, clean and summarize yt transcripts in one go
def summarize_transcript( video_id):
    print(f"Fetching transcript for video id = {video_id}")

    clean_text = fetch_and_clean_transcript(video_id)

    print(f"Cleaned Transcript first 10 character is : {clean_text[0:10]}")

    summary = summarize_text(clean_text)

    print(f"Summary: {summary}")
    
    return summary
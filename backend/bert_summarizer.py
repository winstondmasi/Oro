from textsum.summarize import Summarizer 
from backend.extract_youtube import *

# summarize text using textsum
def summarize_text(input):
    print(f"Input length for text summary is = {len(input)}")
    model = Summarizer()
    
    result = model.summarize_string(input)
    if result:  # Check if the summary is not empty
        print(f"BERT summary result: {result}")
        return result
    else:
        print("Summarizer returned an empty result.")


# fetch, clean and summarize yt transcripts in one go
def summarize_transcript( video_id):
    print(f"Fetching transcript for video id = {video_id}")

    clean_text = fetch_and_clean_transcript(video_id)

    print(f"Cleaned Transcript first 100 character is : {clean_text[0:100]}")

    summary = summarize_text(clean_text)

    print(f"Summary: {summary}")
    
    return summary
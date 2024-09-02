from youtube_transcript_api import YouTubeTranscriptApi 
import re

def parse_youtube_link(url):
    # Patterns for YouTube URLs
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?:live\/)?(?P<id>[^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group('id')
    
    # If no match found, return the original input (assuming it's already a video ID)
    return url


# retrieve the transcript of a given Youtube video
def fetch_transcript(video_id):

    # get basic transcriptfor the language code (en), base case
    yt_transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return yt_transcript

# cleans and concantenate the transcript text
def clean_transcript(transcript):

    strings = []

    for text in transcript:
        for key, value in text.items():
            if key == 'text':
                strings.append(value)

    strings = ' '.join(strings)
    strings = strings.lower()
    return strings


# fetch and clean transcript in one method(step)
def fetch_and_clean_transcript(video_id):
    input = parse_youtube_link(video_id)
    r_transcript = fetch_transcript(input)
    clean_text = clean_transcript(r_transcript)
    return clean_text

from youtube_transcript_api import YouTubeTranscriptApi 

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
    r_transcript = fetch_transcript(video_id)
    clean_text = clean_transcript(r_transcript)
    return clean_text

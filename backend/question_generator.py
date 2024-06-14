from pipeline import pipeline 
from bert_summarizer import *

# generate questiosn based on the provided text
def genetate_questions(text):
    nlp = pipeline("question-generation")
    questions = nlp(text)
    return questions

# generate questions based on the summary from the video id transcript
def generate_questions_from_summary(video_id):
    transcript = summarize_transcript(video_id)
    result = genetate_questions(transcript)
    return result # returns as a list of dictionaries

# covert list of dictionaries result from generate_questions_from_summary to a list of tuples
def dict_to_tuple(dictionary):
    result = []
    for dic in dictionary:
        result.append([dic['question'], dic['answer']])
    return result
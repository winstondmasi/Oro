from question_generation.pipelines import pipeline
from backend.bert_summarizer import *

# generate questiosn based on the provided text
def generate_questions(text):
    nlp = pipeline("question-generation")
    if text is None:
        return []
    questions = nlp(text)
    return questions

# generate questions based on the transcript from the video id transcript
def generate_questions_from_summary(video_id):
    transcript = summarize_text(video_id)
    result = generate_questions(transcript) # returns as a list of dictionaries
    return result 

# covert list of dictionaries result from generate_questions_from_summary to a list of tuples
def dict_to_tuple(dictionary):
    result = []
    for dic in dictionary:
        result.append(tuple([dic['question'], dic['answer']]))
    return result
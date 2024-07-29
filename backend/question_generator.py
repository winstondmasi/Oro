from question_generation.pipelines import pipeline
from backend.bert_summarizer import *

# generate questions based on the transcript from the video id transcript
def generate_questions_from_summary(video_id):
    summary = summarize_transcript(video_id)
    nlp = pipeline("question-generation")
    questions = nlp(summary)
    return questions

# covert list of dictionaries result from generate_questions_from_summary to a list of tuples
def dict_to_tuple(dictionary):
    result = []
    for dic in dictionary:
        result.append(tuple([dic['question'], dic['answer']]))
    return result




''' 
#Simple function to split text into sentences.
def split_into_sentences(text):
    return [s.strip() for s in text.split('.') if s.strip()]

generate questiosn based on the provided text
def generate_questions(text):
    nlp = pipeline("question-generation")
    if text is None:
        return []
    questions = nlp(text)
    return questions
'''
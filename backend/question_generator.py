import re
from backend.bert_summarizer import *

import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

def preprocess_summary(summary):
       # Remove content in parentheses
       summary = re.sub(r'\([^)]*\)', '', summary)
       # Remove extra whitespace
       summary = ' '.join(summary.split())
       return summary

def simple_question_generator(text):
       sentences = sent_tokenize(text)
       questions = []
       for sentence in sentences:
           # Simple transformation: Who/What/When/Where + rest of sentence
           words = sentence.split()
           if len(words) > 3:
               question = f"What {' '.join(words[1:])}?"
               answer = sentence
               questions.append({"question": question, "answer": answer})
       return questions

# generate questions based on the transcript from the video id transcript
def generate_questions_from_summary(video_id):
    summary = summarize_transcript(video_id)
    cleaned_summary = preprocess_summary(summary)
    questions = simple_question_generator(cleaned_summary)
    print("Generated questions:", questions)
    return questions

# covert list of dictionaries result from generate_questions_from_summary to a list of tuples
def dict_to_tuple(dictionary):
    result = []
    for dic in dictionary:
        result.append(tuple([dic['question'], dic['answer']]))
    return result
import datetime
import time
import random
from flask import request
import data_handler


def from_timestamp_datetime(user_questions):
    for question in user_questions:
        question['submission_time'] = datetime.datetime.fromtimestamp(int(question['submission_time'])).strftime('%Y-%m-%d %H:%M:%S')
    return user_questions


def key_generator():
    key = random.randint(1000000,10000000)
    return key


def get_current_timestamp():
    timestamp = time.time()
    return round(timestamp)


def get_current_datetime():
    current_datetime = datetime.datetime.now()
    return current_datetime


def add_question_wrapper():
    question = {
        'id': key_generator(),
        'submission_time': get_current_datetime(),
        'view_number': '0',
        'vote_number': '0',
        'title': request.form.get('title'),
        'message': request.form.get('message'),
        'image': None
    }
    data_handler.add_new_question(question)
    question_id = question['id']
    return question_id


def add_answer_wrapper(question_id):
    answer = {
        'id': key_generator(),
        'submission_time': get_current_datetime(),
        'vote_number': '0',
        'question_id': question_id,
        'message': request.form.get('message')
    }
    data_handler.add_new_answer(answer)
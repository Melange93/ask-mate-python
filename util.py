import datetime
import uuid
import time
from flask import request
import data_handler


def from_timestamp_datetime(user_questions):
    for question in user_questions:
        question['submission_time'] = datetime.datetime.fromtimestamp(int(question['submission_time'])).strftime('%Y-%m-%d %H:%M:%S')
    return user_questions


def key_generator():
    key = uuid.uuid4().hex
    return key


def get_current_timestamp():
    timestamp = time.time()
    return round(timestamp)


def new_question():
    question = {
        'id': key_generator(),
        'submission_time': get_current_timestamp(),
        'view_number': '0',
        'vote_number': '0',
        'title': request.form.get('title'),
        'message': request.form.get('message')
        }
    data_handler.add_user_data(question, data_handler.DATA_FILE_PATH_QUESTIONS, data_handler.DATA_HEADER_QUESTIONS)
    return question

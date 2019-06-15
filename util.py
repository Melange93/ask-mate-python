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


def modify_question():
    question = {
        'id': request.form.get('id'),
        'submission_time': request.form.get('submission_time'),
        'view_number': request.form.get('view_number'),
        'vote_number': request.form.get('vote_number'),
        'title': request.form.get('title'),
        'message': request.form.get('message')
    }
    data_handler.update_user_data(question, data_handler.DATA_FILE_PATH_QUESTIONS, data_handler.DATA_HEADER_QUESTIONS)
    return question


def new_answer(question_id):
    answer = {
        'id': key_generator(),
        'submission_time': get_current_timestamp(),
        'vote_number': '0',
        'question_id': question_id,
        'message': request.form.get('message')
    }
    data_handler.add_user_data(answer, data_handler.DATA_FILE_PATH_ANSWERS, data_handler.DATA_HEADER_ANSWERS)
    return answer


def show_question(question_id):
    user_answers = data_handler.get_all_data(data_handler.DATA_FILE_PATH_ANSWERS, convert_linebreaks=True)
    user_answers = from_timestamp_datetime(user_answers)
    user_questions = data_handler.get_all_data(data_handler.DATA_FILE_PATH_QUESTIONS, convert_linebreaks=True)
    user_questions = from_timestamp_datetime(user_questions)

    for question in user_questions:
        if question['id'] == question_id:
            answers = []
            for answer in user_answers:
                if question['id'] == answer['question_id']:
                    answers.append(answer)
    return question, answers


def cast_vote(casted_id, direction):
    SINGLE_VOTE = 1
    if question_id != 8:
        all_questions = data_handler.get_csv_data(data_handler.DATA_FILE_PATH_QUESTIONS)
        for selected_question in all_questions:
            if selected_question['id'] == question_id:
                question = selected_question
                break
        if direction == "up":
            question['vote_number'] = int(question['vote_number']) + SINGLE_VOTE
            data_handler.update_user_data(question, data_handler.DATA_FILE_PATH_QUESTIONS,
                                          data_handler.DATA_HEADER_QUESTIONS)
        elif down == "down":
            question['vote_number'] = int(question['vote_number']) - SINGLE_VOTE
            data_handler.update_user_data(question, data_handler.DATA_FILE_PATH_QUESTIONS,
                                          data_handler.DATA_HEADER_QUESTIONS)
        return
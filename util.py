import datetime
import uuid


def from_timestamp_datetime(user_questions):
    for question in user_questions:
        question['submission_time'] = datetime.datetime.fromtimestamp(int(question['submission_time'])).strftime('%Y-%m-%d %H:%M:%S')
    return user_questions


def key_generator():
    key = uuid.uuid4().hex
    return key


import datetime
import uuid
import time
import random


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
    timestamp = datetime.datetime.now()
    return timestamp
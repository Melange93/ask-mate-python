import csv
import os
import uuid


DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_all_questions():
    all_user_questions = get_csv_data()

    return all_user_questions


def get_csv_data():
    user_questions = []
    with open(DATA_FILE_PATH, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            user_question = dict(row)

            user_questions.append(user_question)
    return  user_questions


def get_user_story(story_id):
    return  get_csv_data(story_id)


def get_next_id():
    existing_data = get_all_user_story()

    if len(existing_data) == 0:
        return '1'

    return str(int(existing_data[-1]['id']) + 1)


def add_user_story(story):
    story['id'] = get_next_id()
    story['status'] = DEFAULT_STATUS

    add_user_story_to_file(story, True)


def update_user_story(story):
    add_user_story_to_file(story, False)


def add_user_story_to_file(story, append=True):
    existing_data = get_all_user_story()

    with open(DATA_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        writer.writeheader()

        for row in existing_data:

            if not append:
                if int(row['id']) == story['id']:
                    row = story

            writer.writerow(row)

        if append:
            writer.writerow(story)


def convert_linebreaks_to_br(original_str):
    return "<br>".join(original_str.split('\n'))


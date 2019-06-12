import csv
import os
import util


DATA_FILE_PATH_QUESTIONS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
DATA_FILE_PATH_ANSWERS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
DATA_HEADER_QUESTIONS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_ANSWERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_data(convert_linebreaks=False):
    all_user_data = get_csv_data()

    if convert_linebreaks:
        for question in all_user_data:
            question['message'] = convert_linebreaks_to_br(question['message'])

    return all_user_data


def get_csv_data(needed_data):
    user_data = []
    with open(needed_data, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            user_question = dict(row)

            user_data.append(user_question)
    return user_data


def get_user_story(story_id):
    return get_csv_data(story_id)


def get_next_id():
    key = util.key_generator()
    return key


def add_user_story(story):
    story['id'] = get_next_id()
    story['status'] = DEFAULT_STATUS

    add_new_data_to_file(story, True)


def update_user_story(story):
    add_new_data_to_file(story, False)


def add_new_data_to_file(story, needed_data, matching_header, append=True):
    existing_data = get_all_data()

    with open(needed_data, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=matching_header)
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

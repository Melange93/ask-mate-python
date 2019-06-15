import csv
import os
import util


DATA_FILE_PATH_QUESTIONS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
DATA_FILE_PATH_ANSWERS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'answer.csv'
DATA_HEADER_QUESTIONS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_ANSWERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_data(needed_data, convert_linebreaks=False):
    all_user_data = get_csv_data(needed_data)

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


def get_specific_line_data(needed_data, specific_id):
    all_data = get_csv_data(needed_data)
    for selected_data in all_data:
        if selected_data['id'] == specific_id:
            break
    return  selected_data


def add_user_data(data, needed_data, matching_header):
    add_new_data_to_file(data, needed_data, matching_header, True)


def update_user_data(data, needed_data, matching_header):
    add_new_data_to_file(data, needed_data, matching_header, False)


def add_new_data_to_file(story, needed_data, matching_header, append=True):
    existing_data = get_all_data(needed_data)

    with open(needed_data, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=matching_header)
        writer.writeheader()

        for row in existing_data:

            if not append:
                if (row['id']) == story['id']:
                    row = story

            writer.writerow(row)

        if append:
            writer.writerow(story)


def delete_data(story, needed_data, matching_header, answer=False):
    if not answer:
        existing_data = get_all_data(needed_data)

        with open(needed_data, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=matching_header)
            writer.writeheader()

            for row in existing_data:
                if (row['id']) == story['id']:
                    pass
                else:
                    writer.writerow(row)
    if answer:
        existing_data = get_all_data(needed_data)

        with open(needed_data, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=matching_header)
            writer.writeheader()
            for row in existing_data:
                if (row['question_id']) == story['id']:
                    pass
                else:
                    writer.writerow(row)


def convert_linebreaks_to_br(original_str):
    return "<br>".join(original_str.split('\n'))

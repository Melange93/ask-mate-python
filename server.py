from flask import Flask, render_template, request, redirect, url_for


import data_handler
import util


app = Flask(__name__)


@app.route('/list')
def route_list():
    user_questions = data_handler.get_all_data(data_handler.DATA_FILE_PATH_QUESTIONS, convert_linebreaks=True)
    sorted(user_questions, key=lambda question: question['submission_time'], reverse=True)
    user_questions = util.from_timestamp_datetime(user_questions)
    return render_template('list.html', user_questions=user_questions)


@app.route('/ask-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question = {
            'id': util.key_generator(),
            'submission_time': util.get_current_timestamp(),
            'view_number': '0',
            'vote_number': '0',
            'title': request.form.get('title'),
            'message': request.form.get('message')
            }
        data_handler.add_user_data(question, data_handler.DATA_FILE_PATH_QUESTIONS, data_handler.DATA_HEADER_QUESTIONS)
        question_id = question['id']
        return redirect( url_for('view_question', question_id=question_id))

    return render_template('questions.html',
                           form_url=url_for('add_question'),
                           page_title='Ask new question',
                           button_title='Add new question',
                           )


@app.route('/question/<string:question_id>', methods=['GET'])
def view_question(question_id=None):
    user_answers = data_handler.get_all_data(data_handler.DATA_FILE_PATH_ANSWERS, convert_linebreaks=True)
    user_questions = data_handler.get_all_data(data_handler.DATA_FILE_PATH_QUESTIONS, convert_linebreaks=True)
    user_questions = util.from_timestamp_datetime(user_questions)
    for question in user_questions:
        if question['id'] == question_id:
            answers = []
            for answer in user_answers:
                if question['id'] == answer['question_id']:
                    answers.append(answer)
            return render_template('question.html',question=question,
                                    answers=answers)
    return redirect('/list')


@app.route('/question/<string:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        question = {
            'id': request.form.get('id'),
            'submission_time': request.form.get('submission_time'),
            'view_number': request.form.get('view_number'),
            'vote_number': request.form.get('vote_number'),
            'title': request.form.get('title'),
            'message': request.form.get('message')
            }
        data_handler.update_user_data(question, data_handler.DATA_FILE_PATH_QUESTIONS, data_handler.DATA_HEADER_QUESTIONS)
        return redirect('/question/<question_id>')

    all_questions = data_handler.get_csv_data(data_handler.DATA_FILE_PATH_QUESTIONS)
    for selected_question in all_questions:
        if selected_question['id'] == question_id:
            question = selected_question
            break

    return render_template('questions.html',
                           page_title='Edit question',
                           button_title='Edit question',
                           question=question,
                           question_id=question_id
                           )


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )

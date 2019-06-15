from flask import Flask, render_template, request, redirect, url_for
import data_handler
import util


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    user_questions = data_handler.get_all_data(data_handler.DATA_FILE_PATH_QUESTIONS, convert_linebreaks=True)
    user_questions.sort(key=lambda question: question['submission_time'], reverse=True)
    user_questions = util.from_timestamp_datetime(user_questions)
    return render_template('list.html', user_questions=user_questions)


@app.route('/ask-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question = util.new_question()
        question_id = question['id']
        return redirect(url_for('view_question', question_id=question_id))

    return render_template('questions.html',
                           form_url=url_for('add_question'),
                           page_title='Ask new question',
                           button_title='Add new question',
                           )


@app.route('/question/<string:question_id>', methods=['GET'])
def view_question(question_id=None):
    q_and_a = util.show_question(question_id)
    return render_template('question.html', question=q_and_a[0],
                            answers=q_and_a[1])


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id=None):
    if request.method == 'POST':
        answer = util.new_answer(question_id)
        return redirect(url_for('view_question', question_id=answer['question_id']))

    return render_template('new-answer.html', question_id=question_id)


@app.route('/question/<string:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        question = util.modify_question()
        return redirect(url_for('view_question', question_id=question['id']))

    question = data_handler.get_specific_line_data(data_handler.DATA_FILE_PATH_QUESTIONS, question_id)
    return render_template('questions.html',
                           page_title='Edit question',
                           button_title='Edit question',
                           question=question,
                           question_id=question_id
                           )


@app.route('/answer/<answer_id>/vote-<down>', methods=['GET', 'POST'])
@app.route('/answer/<answer_id>/vote-<up>', methods=['GET', 'POST'])
@app.route('/question/<question_id>/vote-<down>', methods=['GET', 'POST'])
@app.route('/question/<question_id>/vote-<up>', methods=['GET', 'POST'])
def vote(question_id=None, answer_id=None, up=None):
    SINGLE_VOTE = 1
    if request.method == 'POST':
        if question_id and not answer_id:
            all_questions = data_handler.get_csv_data(data_handler.DATA_FILE_PATH_QUESTIONS)
            for selected_question in all_questions:
                if selected_question['id'] == question_id:
                    question = selected_question
                    break
            if up == "up":
                question['vote_number'] = int(question['vote_number']) + SINGLE_VOTE
                data_handler.update_user_data(question, data_handler.DATA_FILE_PATH_QUESTIONS, data_handler.DATA_HEADER_QUESTIONS)
            else:
                question['vote_number'] = int(question['vote_number']) - SINGLE_VOTE
                data_handler.update_user_data(question, data_handler.DATA_FILE_PATH_QUESTIONS, data_handler.DATA_HEADER_QUESTIONS)
            return redirect(url_for('view_question', question_id=question_id))
        if answer_id and not question_id:
            all_answers = data_handler.get_csv_data(data_handler.DATA_FILE_PATH_ANSWERS)
            for selected_answer in all_answers:
                if selected_answer['id'] == answer_id:
                    answer = selected_answer
                    break
            if up == "up":
                answer['vote_number'] = int(answer['vote_number']) + SINGLE_VOTE
                data_handler.update_user_data(answer, data_handler.DATA_FILE_PATH_ANSWERS, data_handler.DATA_HEADER_ANSWERS)
            else:
                answer['vote_number'] = int(answer['vote_number']) - SINGLE_VOTE
                data_handler.update_user_data(answer, data_handler.DATA_FILE_PATH_ANSWERS, data_handler.DATA_HEADER_ANSWERS)
            return redirect(url_for('view_question', question_id=answer['question_id']))


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def del_record(question_id):
    all_questions = data_handler.get_csv_data(data_handler.DATA_FILE_PATH_QUESTIONS)

    if request.method == 'POST':
        for question in all_questions:
            if question_id == question:
                pass

        data_handler.delete_data(question, data_handler.DATA_FILE_PATH_QUESTIONS, data_handler.DATA_HEADER_QUESTIONS)

        data_handler.delete_data(question, data_handler.DATA_FILE_PATH_ANSWERS, data_handler.DATA_HEADER_ANSWERS, True)

        return redirect('/list')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )

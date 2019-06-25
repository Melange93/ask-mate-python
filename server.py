from flask import Flask, render_template, request, redirect, url_for
import data_handler
import util


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    user_questions = data_handler.get_questions()
    return render_template('list.html', user_questions=user_questions)


@app.route('/ask-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question = {
            'id': util.key_generator(),
            'submission_time': util.get_current_datetime(),
            'view_number': '0',
            'vote_number': '0',
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'image': None
            }
        data_handler.add_new_question(question)
        question_id = question['id']
        return redirect(url_for('view_question', question_id=question_id))

    return render_template('add_edit_questions.html',
                           form_url=url_for('add_question'),
                           page_title='Ask new question',
                           button_title='Add new question',
                           )


@app.route('/question/<string:question_id>', methods=['GET'])
def view_question(question_id=None):
    answers = data_handler.get_answer_data_by_id(question_id)
    user_question = data_handler.get_question_data_by_id(question_id)[0]
    return render_template('question.html', user_question=user_question,
                                    answers=answers)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id=None):
    if request.method == 'POST':
        answer = {
            'id': util.key_generator(),
            'submission_time': util.get_current_timestamp(),
            'vote_number': '0',
            'question_id': question_id,
            'message': request.form.get('message')
            }
        data_handler.add_user_data(answer, data_handler.DATA_FILE_PATH_ANSWERS, data_handler.DATA_HEADER_ANSWERS)
        return redirect( url_for('view_question', question_id=question_id))

    return render_template('new-answer.html', question_id=question_id)


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
        temp = data_handler.edit_question(question)
        return redirect( url_for('view_question', question_id=question_id))

    question = data_handler.get_question_data_by_id(question_id)[0]

    return render_template('add_edit_questions.html',
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
            question = data_handler.get_vote_number_question(question_id)[0]
            if up == "up":
                question['vote_number'] = int(question['vote_number']) + SINGLE_VOTE
                data_handler.set_vote_question(question['id'], question['vote_number'])
            else:
                question['vote_number'] = int(question['vote_number']) - SINGLE_VOTE
                data_handler.set_vote_question(question['id'], question['vote_number'])
            return redirect(url_for('view_question', question_id=question_id))
        if answer_id and not question_id:
            answer = data_handler.get_vote_number_answer(answer_id)[0]
            if up == "up":
                answer['vote_number'] = int(answer['vote_number']) + SINGLE_VOTE
                data_handler.set_vote_answer(answer['id'], answer['vote_number'])
            else:
                answer['vote_number'] = int(answer['vote_number']) - SINGLE_VOTE
                data_handler.set_vote_answer(answer['id'], answer['vote_number'])
            return redirect(url_for('view_question', question_id=answer['question_id']))


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def del_record(question_id):
    data_handler.delete_question(question_id)
    return redirect('/list')


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
    )

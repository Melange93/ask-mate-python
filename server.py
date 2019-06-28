from flask import Flask, render_template, request, redirect, url_for
import data_handler
import util


app = Flask(__name__)


@app.route('/')
def show_top_5_questions():
    LIMIT_NUMBER = 5
    user_questions = data_handler.get_limited_questions(LIMIT_NUMBER)
    return render_template('list.html', user_questions=user_questions, limit_number=LIMIT_NUMBER)


@app.route('/list')
def route_list():
    user_questions = data_handler.get_questions()
    return render_template('list.html', user_questions=user_questions)


@app.route('/ask-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question_id = util.add_question_wrapper()
        return redirect(url_for('view_question', question_id=question_id))

    return render_template('add_edit_questions.html',
                           form_url=url_for('add_question'),
                           page_title='Ask new question',
                           button_title='Submit question',
                           )


@app.route('/question/<string:question_id>', methods=['GET'])
def view_question(question_id=None):
    answers = data_handler.get_answer_data_by_id(question_id)
    user_question = data_handler.get_question_data_by_id(question_id)[0]
    question_comments = data_handler.get_comments_for_question(question_id)
    #answer_comments = data_handler.get_comments_for_answers(answer_id)
    return render_template('question.html',
                           user_question=user_question,
                           answers=answers,
                           question_comments=question_comments)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id=None):
    if request.method == 'POST':
        answer = {
            'id': util.key_generator(),
            'submission_time': util.get_current_datetime(),
            'vote_number': '0',
            'question_id': question_id,
            'message': request.form.get('message')
            }
        data_handler.add_new_answer(answer)
        return redirect(url_for('view_question', question_id=question_id))

    return render_template('add_edit_answer.html',
                           page_title='Add answer',
                           button_title='Submit answer',
                           question_id=question_id)


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
        data_handler.edit_question(question)
        return redirect(url_for('view_question', question_id=question_id))

    question = data_handler.get_question_data_by_id(question_id)[0]

    return render_template('add_edit_questions.html',
                           page_title='Edit question',
                           button_title='Edit question',
                           question=question,
                           question_id=question_id
                           )


@app.route('/answer/<answer_id>/vote-<down>', methods=['POST'])
@app.route('/answer/<answer_id>/vote-<up>', methods=['POST'])
@app.route('/question/<question_id>/vote-<down>', methods=['POST'])
@app.route('/question/<question_id>/vote-<up>', methods=['POST'])
def vote(question_id=None, answer_id=None, up=None):
    SINGLE_VOTE = 1

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


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'POST':
        answer = data_handler.get_answer_data_by_answer_id(answer_id)[0]
        answer['message'] = request.form.get('message')
        data_handler.edit_answer(answer)
        return redirect(url_for('view_question', question_id=answer['question_id']))

    answer = data_handler.get_answer_data_by_answer_id(answer_id)[0]

    return render_template('add_edit_answer.html',
                           page_title='Edit answer',
                           button_title='Edit answer',
                           answer=answer
                           )


@app.route('/search', methods=['GET'])
def search():
    searched_string = request.args["searched_string"]
    q_results = data_handler.search_questions(searched_string)
    a_results = data_handler.search_answers(searched_string)
    return render_template('search.html', q_results=q_results, a_results=a_results, searched_string=searched_string)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def new_question_comment(question_id=None):
    if request.method == 'POST':
        question_comment = {
            'id': util.key_generator(),
            'question_id': question_id,
            'message': request.form.get('message'),
            'submission_time': util.get_current_datetime(),
            'edited_count': '0'
             }
        data_handler.add_new_question_comment(question_comment)
        return redirect(url_for('view_question', question_id=question_id))

    return render_template('add_edit_question_answer_comments.html',
                           page_title='Add comment to question',
                           button_title='Submit comment',
                           question_id=question_id)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def new_answer_comment(answer_id=None):
    if request.method == 'POST':
        answer_comment = {
            'id': util.key_generator(),
            'answer_id': answer_id,
            'message': request.form.get('message'),
            'submission_time': util.get_current_datetime(),
            'edited_count': '0'
             }
        data_handler.add_new_answer_comment(answer_comment)
        question_id = data_handler.get_answer_data_by_answer_id(answer_id)[0]
        return redirect(url_for('view_question', question_id=question_id['question_id']))

    return render_template('add_edit_question_answer_comments.html',
                           page_title='Add comment to answer',
                           button_title='Submit comment',
                           answer_id=answer_id)


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
    )

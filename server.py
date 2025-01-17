from flask import Flask, render_template, request, redirect, url_for, session, escape
import data_handler
import util
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def show_top_5_questions():
    LIMIT_NUMBER = 5
    user_questions = data_handler.get_limited_questions(LIMIT_NUMBER)
    if 'user' in session:
        username = escape(session['user'])
        return render_template('list.html', user_questions=user_questions, limit_number=LIMIT_NUMBER, username=username)
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
    answers = data_handler.get_answer_data_comments_by_id(question_id)
    answers1 = data_handler.get_answer_data_by_id(question_id)
    user_question = data_handler.get_question_data_by_id(question_id)[0]
    answers_ids = []
    for answer in answers:
        for key, value in answer.items():
            if key == 'id':
                answers_ids.append(value)
    comments = [data_handler.get_comments_for_answers(id_) for id_ in answers_ids]

    question_comments = data_handler.get_comments_for_question(question_id)
    question_tag = data_handler.get_tags(question_id)
    tags_ids = []
    for element in question_tag:
        tags_ids.append(element['tag_id'])
    tags_names = [data_handler.get_question_tags(id_) for id_ in tags_ids]
    return render_template('question.html',
                           user_question=user_question,
                           answers=answers,
                           question_comments=question_comments,
                           tags_names=tags_names,
                           comments=comments,
                           answers1=answers1
                           )


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id=None):
    if request.method == 'POST':
        util.add_answer_wrapper(question_id)
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


@app.route('/question/<question_id>/vote-<down>', methods=['POST'])
@app.route('/question/<question_id>/vote-<up>', methods=['POST'])
def vote_question(question_id=None, up=None):
    SINGLE_VOTE = 1

    question = data_handler.get_vote_number_question(question_id)[0]
    if up == "up":
        question['vote_number'] = int(question['vote_number']) + SINGLE_VOTE
        data_handler.set_vote_question(question['id'], question['vote_number'])
    else:
        question['vote_number'] = int(question['vote_number']) - SINGLE_VOTE
        data_handler.set_vote_question(question['id'], question['vote_number'])
    return redirect(url_for('view_question', question_id=question_id))


@app.route('/answer/<answer_id>/vote-<down>', methods=['POST'])
@app.route('/answer/<answer_id>/vote-<up>', methods=['POST'])
def vote_answer(answer_id=None, up=None):
    SINGLE_VOTE = 1

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


@app.route('/question/<question_id>/add_tag', methods=['POST', 'GET'])
def add_new_tag(question_id = None):
    if request.method == 'POST':
        tag = {
            'tag_id': util.key_generator(),
            'tag_name': request.form.get('tag_name'),
            'question_id': question_id
        }
        print(tag['tag_name'])
        data_handler.add_new_tag(tag)
        data_handler.add_new_question_tag(tag)
        return redirect(url_for('view_question', question_id=question_id))

    return render_template('add_new_tag.html',
                           page_title='Add new tag',
                           button_title='Submit tag',
                           question_id=question_id)


@app.route('/comments/<comment_id>/delete', methods=['GET'])
def del_comment(comment_id):
    q_and_a_id = data_handler.get_q_and_a_id_from_comment(comment_id)
    data_handler.delete_comment(comment_id)
    if q_and_a_id[0]['answer_id']:
        answer_id = q_and_a_id[0]['answer_id']
        question_id = data_handler.get_question_id_from_answer_id(answer_id)
        question_id = question_id[0]['id']
    else:
        question_id = q_and_a_id[0]['question_id']
    return redirect(url_for('view_question', question_id=question_id))


@app.route('/answer/<answer_id>/delete', methods=['GET'])
def del_answer(answer_id):
    question_id = data_handler.get_answer_data_by_answer_id(answer_id)[0]
    data_handler.delete_answer(answer_id)
    return redirect(url_for('view_question', question_id=question_id['question_id']))


@app.route('/<question_id>/comments/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(question_id=None, comment_id=None):
    if request.method == 'POST':
        comment = data_handler.get_comment(comment_id)[0]
        comment['message'] = request.form.get('message')
        comment['edited_count'] += 1
        data_handler.edit_comment(comment)
        return redirect(url_for('view_question', question_id=question_id))

    comment = data_handler.get_comment(comment_id)[0]

    return render_template('add_edit_question_answer_comments.html',
                           page_title='Edit comment',
                           button_title='Edit comment',
                           comment=comment,
                           question_id=question_id
                           )

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        user = {
            'id': util.key_generator(),
            'registration_time': util.get_current_datetime(),
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': util.hash_password(request.form.get('password')),
            'role': 'user'
        }
        data_handler.add_new_user(user)
        return redirect(url_for('route_list'))

    return render_template('registration.html',
                           page_title='Registration',
                           button_title='Registrate')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = {
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }
        hashed_password = data_handler.get_password(user)
        verified = util.verify_password(user['username'], hashed_password[0]['password'])
        if verified:
            user_all_data = data_handler.get_user_data(user)
            session['user'] = user_all_data[0]['username']

            return redirect(url_for('route_list'))

        else:
            return redirect(url_for('route_list'))
    return render_template('login.html',
                           page_title='Login',
                           button_title='Login')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    print(session['user'])
    session.pop('user', None)
    return redirect(url_for('route_list'))


@app.route('/listallusers')
def list_all_users():
    if not session or session['user'] != "admin":
        return redirect(url_for('route_list'))
    if session['user'] == "admin":
        all_users_data = data_handler.get_all_users()
        return render_template('listallusers.html',
                               page_title='List of all users',
                               all_users_data=all_users_data)


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
    )

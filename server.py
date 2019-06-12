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
            'id': request.form.get('id'),
            'submission_time': util.get_current_timestamp(),
            'view_number': '0',
            'vote_number': '0',
            'title': request.form.get('title'),
            'message': request.form.get('message')
            }
        data_handler.add_user_data(question, data_handler.DATA_FILE_PATH_QUESTIONS, data_handler.DATA_HEADER_QUESTIONS)
        return redirect('/list')

    return render_template('questions.html',
                           form_url=url_for('add_question'),
                           page_title='Ask new question',
                           button_title='Add new question',
                           )


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def view_question(question_id):
    if request.method == 'POST':

        if int(request.form.get('id')) != story_id:
            raise ValueError('The recieved ID is not valid!')

        user_story = {
            'id': story_id,
            'title': request.form.get('title'),
            'user_story': request.form.get('user_story'),
            'acceptance_criteria': request.form.get('acceptance_criteria'),
            'business_value': request.form.get('business_value') + " point",
            'estimation': request.form.get('estimation') + "h",
            'status': request.form.get('status')
        }

        data_handler.update_user_story(user_story)
        return redirect('/')

    # user_story = data_handler.get_user_story(story_id)

    user_story = data_handler.get_csv_data(story_id)
    return render_template('story.html',
                           form_url=url_for('add_story'),
                           page_title='Edit User Story',
                           button_title='Edit User Story',
                           user_story=user_story,
                           statuses=data_handler.STATUSES,
                           selected_status=user_story['status']
                           )


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )

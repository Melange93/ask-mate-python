import database_common


@database_common.connection_handler
def get_vote_number_question(cursor, id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %s;
                   """,
                   (id, ))
    question = cursor.fetchall()
    return question


@database_common.connection_handler
def set_vote_question(cursor, id, vote_number):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = %s
                    WHERE id = %s;
                   """,
                   (vote_number, id,))


@database_common.connection_handler
def get_vote_number_answer(cursor, id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %s;
                   """,
                   (id, ))
    question = cursor.fetchall()
    return question


@database_common.connection_handler
def set_vote_answer(cursor, id, vote_number):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = %s
                    WHERE id = %s;
                   """,
                   (vote_number, id,))


@database_common.connection_handler
def get_comments(cursor, question_id, answer_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id = %s;
                   """,
                   (question_id,)
                   )
    cursor.execute("""
                        SELECT * FROM comment
                        WHERE answer_id = %s;
                       """,
                   (answer_id,)
                   )
    comments = cursor.fetchall()
    return comments


@database_common.connection_handler
def delete_question(cursor, question_id):

    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %s;
                   """,
                   (question_id,))


@database_common.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC;
                   """
                   )
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_answer(cursor):
    cursor.execute("""
                    SELECT * FROM answer
                    ORDER BY submission_time ASC;
                   """
                   )
    answer = cursor.fetchall()
    return answer


@database_common.connection_handler
def get_question_data_by_id(cursor, id_):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %s;
                   """,
                   (id_,)
                   )
    question_data = cursor.fetchall()
    return question_data


@database_common.connection_handler
def get_answer_data_by_id(cursor, id_):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %s ORDER BY submission_time ASC;
                   """,
                   (id_,)
                   )
    answer_data = cursor.fetchall()
    return answer_data


@database_common.connection_handler
def add_new_question(cursor, question):
    cursor.execute("""
                    INSERT INTO question
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                   (question['id'],
                    question['submission_time'],
                    question['view_number'],
                    question['vote_number'],
                    question['title'],
                    question['message'],
                    question['image']
                        )
                    )


@database_common.connection_handler
def edit_question(cursor, question):
    cursor.execute("""
                    UPDATE question
                    SET title = %s, message = %s
                    WHERE id = %s;
                   """,
                   (question['title'], question['message'], question['id'],))


@database_common.connection_handler
def get_limited_questions(cursor, limit_number):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC LIMIT %s;
                   """,
                   (limit_number,)
                   )
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def add_new_answer(cursor, answer):
    cursor.execute("""
                    INSERT INTO answer
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                   (answer['id'],
                    answer['submission_time'],
                    answer['vote_number'],
                    answer['question_id'],
                    answer['message']
                        )
                    )


@database_common.connection_handler
def edit_answer(cursor, answer):
    cursor.execute("""
                    UPDATE answer
                    SET message = %s
                    WHERE id = %s;
                   """,
                   (answer['message'], answer['id'],))


@database_common.connection_handler
def get_answer_data_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %s;
                   """,
                   (answer_id,)
                   )
    answer_data = cursor.fetchall()
    return answer_data


@database_common.connection_handler
def search_questions(cursor, searched_string):
    cursor.execute("""
                    SELECT * 
                      FROM question
                     WHERE title LIKE %(searched_string)s OR message LIKE %(searched_string)s
                    """,
                   {'searched_string': '%' + searched_string + '%'})
    return cursor.fetchall()


@database_common.connection_handler
def search_answers(cursor, searched_string):
    cursor.execute("""
                    SELECT * 
                      FROM answer
                     WHERE message LIKE %(searched_string)s
                    """,
                   {'searched_string': '%' + searched_string + '%'})
    return cursor.fetchall()


@database_common.connection_handler
def add_new_question_comment(cursor, question_comment):
    cursor.execute("""
                    INSERT INTO comment (id, question_id, message, submission_time, edited_count)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                   (question_comment['id'],
                    question_comment['question_id'],
                    question_comment['message'],
                    question_comment['submission_time'],
                    question_comment['edited_count'],
                        )
                    )


@database_common.connection_handler
def add_new_answer_comment(cursor, answer_comment):
    cursor.execute("""
                    INSERT INTO comment (id, answer_id, message, submission_time, edited_count)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                   (answer_comment['id'],
                    answer_comment['answer_id'],
                    answer_comment['message'],
                    answer_comment['submission_time'],
                    answer_comment['edited_count'],
                        )
                    )


@database_common.connection_handler
def get_comments_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id = %s ORDER BY submission_time ASC;
                   """,
                   (question_id,)
                   )
    question_comments = cursor.fetchall()
    return question_comments


@database_common.connection_handler
def get_comments_for_answers(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE answer_id = %s ORDER BY submission_time ASC;
                   """,
                   (answer_id,)
                   )
    answers_comments = cursor.fetchall()
    return answers_comments


@database_common.connection_handler
def delete_comment(cursor, comment_id):

    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %s;
                   """,
                   (comment_id,))


@database_common.connection_handler
def get_q_and_a_id_from_comment(cursor, comment_id):
    cursor.execute("""
                    SELECT question_id,answer_id FROM comment
                    WHERE id = %s;
                   """,
                   (comment_id,)
                   )
    question_id = cursor.fetchall()
    return question_id


@database_common.connection_handler
def delete_answer(cursor, answer_id):

    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %s;
                   """,
                   (answer_id,))


@database_common.connection_handler
def add_new_tag(cursor, tag):
    cursor.execute("""
                    INSERT INTO tag
                    VALUES (%s, %s)
    
                   """,
                   (tag['tag_id'],
                    tag['tag_name'],
                    )
                   )

@database_common.connection_handler
def add_new_question_tag(cursor, tag):
    cursor.execute("""
                        INSERT INTO question_tag
                        VALUES (%s, %s)

                       """,
                   (tag['question_id'],
                    tag['tag_id'],
                    )
                   )
@database_common.connection_handler
def get_tags(cursor, input_id_):
    cursor.execute("""
                    SELECT question_id, tag_id FROM question_tag
                    WHERE question_id = %s;
                   """,
                   (input_id_,)
                   )
    tags = cursor.fetchall()
    return tags


@database_common.connection_handler
def get_question_tags(cursor, id_):
    cursor.execute("""
                    SELECT name FROM tag
                    WHERE id = %s;
                   """,
                   (id_,)
                   )
    question_tags = cursor.fetchall()
    return question_tags


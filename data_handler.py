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
def delete_question(cursor, question_id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %s;
                   """,
                   (question_id,))
    cursor.execute("""
                        DELETE FROM answer
                        WHERE question_id = %s;
                       """,
                   (question_id,))


@database_common.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time ASC;
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
import database_common


@database_common.connection_handler
def get_vote_number(cursor, needed_table, id):
    cursor.execute("""
                    SELECT vote_number FROM needed_table
                    WHERE id = %s;
                   """,
                   (needed_table, id, ))
    vote_number = cursor.fetchall()
    return vote_number


@database_common.connection_handler
def set_vote(cursor, vote, needed_table, id):
    cursor.execute("""
                    UPDATE %s
                    SET vote_number = %s
                    WHERE id = %s;
                   """,
                   (needed_table, vote, id))


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
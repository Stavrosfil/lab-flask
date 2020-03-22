import sqlite3

db = sqlite3.connect("../instance/users.db")
db2 = sqlite3.connect("../instance/users_flask.db")


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()

    return rows


def copy_users(conn, user):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = """ INSERT INTO users(user_id,
                                second_id,
                                first_name,
                                last_name,
                                mm_username,
                                project,
                                administrator)
              VALUES(?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid


def init_db(conn):
    c = conn.cursor()
    with open("../laboratorium/schema.sql") as f:
        db2.executescript(f.read())


init_db(db2)

for user in select_all_tasks(db):
    user = (user[0], user[1], user[2], user[3], user[4], user[8], 0)
    print(user)
    copy_users(db2, user)
    db2.commit()

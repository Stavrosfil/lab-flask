# ------------------------------ SQLITE DATABASE ----------------------------- #

import sqlite3

import click
from flask import g, current_app as app
from flask.cli import with_appcontext


# -------------------------------- FUNCTIONAL -------------------------------- #

def query_db(query, db, args=(), one=False):
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_user(user_id, db, args=()):
    cur = db.execute(
        "select * from users where user_id = '{}'".format(user_id), args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None)


@app.route("/test")
def testRoute():
    user = get_user('79382C83')
    print(user["first_name"])
    return user['mm_username']


# ------------------------------- OPEN-CLOSE DB ------------------------------ #


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
            check_same_thread=False
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# ------------------------------ INITIALIZATION ------------------------------ #

def init_app():
    # Tell flask to call this when cleaning up
    app.teardown_appcontext(close_db)
    # Create a flask command called `init-db` that calls init_db()
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_db():
    db = get_db()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#         db.row_factory = sqlite3.Row
#     return db


# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()


# def make_dicts(cursor, row):
#     return dict((cursor.description[idx][0], value)
#                 for idx, value in enumerate(row))

# ------------------------------ SQLITE DATABASE ----------------------------- #

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_app(app):
    # Tell flask to call this when cleaning up
    app.teardown_appcontext(close_db)
    # Create a flask command called `init-db` that calls init_db()
    app.cli.add_command(init_db_command)


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# DATABASE = 'users.db'

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


# def query_db(query, args=(), one=False):
#     cur = get_db().execute(query, args)
#     rv = cur.fetchall()
#     cur.close()
#     return (rv[0] if rv else None) if one else rv


# def get_user(user_id, args=(), one=False):
#     cur = get_db().execute(
#         "select * from users where user_id = '{}'".format(user_id), args)
#     rv = cur.fetchall()
#     cur.close()
#     return (rv[0] if rv else None) if one else rv

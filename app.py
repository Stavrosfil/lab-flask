"""

A small Test application to show how to use Flask-MQTT.

"""

import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

import sqlite3
from sqlite3 import Error
from flask import g

eventlet.monkey_patch()

app = Flask(__name__)
# app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '52.143.162.206'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_CLEAN_SESSION'] = False

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_CA_CERTS'] = "ca.crt"
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    with app.app_context():

        mqtt.subscribe('asat_lab/user_auth/test')
        mqtt.publish('asat_lab/user_auth/test', '{"user_id": "79382C83"}')
        # db = get_db()
        out = ""
        for user in query_db('select * from users'):
            print(user)
            out += "<p> {} {} \t ({}) has the id {} </p>".format(
                user['first_name'], user['last_name'], user['mm_username'], user['user_id'])
            # print(user['first_name'], 'has the id', user['user_id'])

        print(out)

        # test = db.row_factory = make_dicts
        # r = db.row_factory = sqlite3.Row[1]
        # print(db)
        # print(db.row_factory[1])
        # for value in r:
        # print(value)

        # return render_template('index.html')
    return out


# ----------------------------------- MQTT ----------------------------------- #

@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'])


@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )

    with app.app_context():
        user_id = json.loads(message.payload.decode())['user_id']
        print(user_id)
        user = get_user(user_id)[0]
        print(user["mm_username"])

    socketio.emit('mqtt_message', data=data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


# ------------------------------ SQLITE DATABASE ----------------------------- #

DATABASE = 'users.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_user(user_id, args=(), one=False):
    cur = get_db().execute(
        "select * from users where user_id = '{}'".format(user_id), args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


if __name__ == '__main__':
    # important: Do not use reloader because this will create two Flask instances.
    # Flask-MQTT only supports running with one instance
    socketio.run(app, host='0.0.0.0', port=5000,
                 use_reloader=True, debug=False)

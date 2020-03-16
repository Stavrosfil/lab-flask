# ----------------------------------- MQTT ----------------------------------- #
from flask_mqtt import Mqtt
from flask import g, current_app as app
import json
from laboratorium.db import get_db, get_user


mqtt = Mqtt(app)
db = get_db()


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('testopic')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )

    user_id = json.loads(message.payload.decode())['user_id']
    user = get_user(user_id, db)
    print(user["mm_username"])


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


# def get_mqttc():
#     if 'mqttc' not in g:
#         mqtt = Mqtt(app)
#         g.mqttc = mqtt
#     return g.mqttc

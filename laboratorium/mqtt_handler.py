# ----------------------------------- MQTT ----------------------------------- #
from flask_mqtt import Mqtt
from flask import g, current_app as app
import json
from laboratorium.db import get_db, get_user
from laboratorium import r
from laboratorium.helpers import user_handler


mqtt = Mqtt(app, True)
db = get_db()


MQTT_RFID = app.config['MQTT_RFID_TOPIC']
MQTT_RESPONSE = app.config['MQTT_RFID_RESP_TOPIC']


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(MQTT_RFID)


@mqtt.on_topic(MQTT_RFID)
def handle_checkin(client, userdata, message):

    user_id = json.loads(message.payload.decode())['user_id']
    user = get_user(user_id, db)

    resp = user_handler(user)

    print(resp)

    mqtt.publish(MQTT_RESPONSE, json.dumps(resp))


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


# def get_mqttc():
#     if 'mqttc' not in g:
#         mqtt = Mqtt(app)
#         g.mqttc = mqtt
#     return g.mqttc

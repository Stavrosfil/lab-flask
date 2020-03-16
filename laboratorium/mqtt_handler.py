# ----------------------------------- MQTT ----------------------------------- #
from flask_mqtt import Mqtt
from flask import g, current_app as app
import json
from laboratorium.db import get_db, get_user
from laboratorium import r


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

    in_lab = "{}:in_lab".format(user_id)
    if r.get(in_lab) == b'0':
        r.set(in_lab, 1)
    else:
        r.set(in_lab, 0)

    resp = {}
    resp["user_name"] = "{} {}.".format(
        user['last_name'], user['first_name'][0])
    resp["direction"] = int(r.get(in_lab))

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

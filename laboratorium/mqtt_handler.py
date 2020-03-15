# ----------------------------------- MQTT ----------------------------------- #
from flask_mqtt import Mqtt
from flask import g, current_app as app
import json
from . import db


def init_mqtt():

    mqtt = get_mqttc()

    @app.route('/mqttest')
    def hello2():
        mqtt.publish("testopic", "another test")
        return("Im not here")

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
        print(user_id)
        user = db.get_user(user_id)
        # print(user["mm_username"])
        print("test")

    @mqtt.on_log()
    def handle_logging(client, userdata, level, buf):
        print(level, buf)


def get_mqttc():
    if 'mqttc' not in g:
        mqtt = Mqtt(app)
        g.mqttc = mqtt
    return g.mqttc

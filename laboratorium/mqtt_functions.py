from laboratorium import mongo, User, mqtt
import json

mqtt.subscribe('laboratorium/lab1/auth/rfid')
mqtt.publish('laboratorium/lab1/auth/response', 'Connection established')

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('laboratorium/lab1/auth/rfid')
    mqtt.publish('laboratorium/lab1/auth/response', 'Connection established')
    print('-'*20)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=json.loads(message.payload.decode())
    )
    response = {'user_name': data['payload']['user_id'], 'direction': 1}
    print(response)
    mqtt.publish('laboratorium/lab1/auth/response', json.dumps(response)) 

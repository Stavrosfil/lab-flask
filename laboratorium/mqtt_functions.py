from laboratorium import mongo, User, mqtt, mongo_functions
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
    # data = dict(
    #     topic=message.topic,
    #     payload=json.loads(message.payload.decode())
    # )
    tag_uuid = json.loads(message.payload.decode())['user_id']
    user = mongo_functions.checkin_by_tag('1', tag_uuid)
    response = {'user_name': user.first_name, 'direction': user.lab_uuid}
    # print(response)
    mqtt.publish('laboratorium/lab1/auth/response', json.dumps(response)) 

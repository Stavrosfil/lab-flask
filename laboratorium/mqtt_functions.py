from laboratorium import mongo, User, mqtt, mongo_functions
import json
from pprint import pprint

mqtt.subscribe('laboratorium/lab1/auth/rfid')
data = {'top_line': 'Connection', 'bottom_line': 'established'}
mqtt.publish('laboratorium/lab1/auth/response', json.dumps(data))
    
# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     mqtt.subscribe('laboratorium/lab1/auth/rfid')
#     mqtt_publish_json('laboratorium/lab1/auth/response', {'top_line': 'Connection', 'bottom_line': 'established'})
#     print('-'*20)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    # data = dict(
    #     topic=message.topic,
    #     payload=json.loads(message.payload.decode())
    # )
    payload = json.loads(message.payload.decode())
    user = User.User(payload)
    
    device_uuid = payload['device_uuid']

    user.checkin(lab_uuid=device_uuid)

    response = {
        'lab_uuid': user.lab_uuid,
        'top_line': "Welcome" if user.lab_uuid != '0' else "Goodbye",
        'bottom_line': "{} {}.".format(user.last_name, user.first_name[0]),
    }
    pprint(message)
    mqtt.publish('laboratorium/lab1/auth/response', json.dumps(response)) 

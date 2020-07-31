from laboratorium import mongo, User, mqtt, mongo_functions
import json, requests

mqtt.subscribe('laboratorium/lab1/auth/rfid')
data = {'top_line': 'Connection', 'bottom_line': 'established'}
mqtt.publish('laboratorium/lab1/auth/response', json.dumps(data))
    
# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     mqtt.subscribe('laboratorium/lab1/auth/rfid')
#     mqtt_publish_json('laboratorium/lab1/auth/response', {'top_line': 'Connection', 'bottom_line': 'established'})
#     print('-'*20)

 
def postHook(message):
    dictToSend = {'text': message, 'username': 'Lab Opener'}

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    # app.logger.info(buf)
    print(buf)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    # data = dict(
    #     topic=message.topic,
    #     payload=json.loads(message.payload.decode())
    # )
    payload = json.loads(message.payload.decode())
    user = User.User(payload)
    device_uuid = payload['device_uuid']
    lab = mongo_functions.get_lab_by_device(device_uuid)
    lab_uuid = lab.get('_id')
    
    if payload['tag_uuid'][0] == 'C9D3A847':
        mongo_functions.remove_all_from_lab()
        
    if user.user_uuid != "":
    
        user.checkin(lab_uuid)
    
        response = {
            'lab_uuid': user.lab_uuid,
            'top_line': "Welcome" if user.lab_uuid != '0' else "Goodbye",
            'bottom_line': "{} {}.".format(user.last_name, user.first_name[0]),
        }
        mqtt.publish('laboratorium/lab1/auth/response', json.dumps(response)) 
    else:
        response = {
            'lab_uuid': user.lab_uuid,
            'top_line': "Error",
            'bottom_line': "Unknown User"
        }
        mqtt.publish('laboratorium/lab1/auth/response', json.dumps(response)) 

    population = mongo_functions.get_lab_population(lab_uuid) 

    if population == 0:
        message = f"The lab just closed!"
        postHook(message)
    elif population == 1 and user.lab_uuid == lab_uuid:
        message = f"The lab just opened by @{user.mm_username}!\n\nReact and you are invited!"
        postHook(message)
    

from laboratorium import mongo, User, mqtt, mongo_functions, hooks, queue
import json, requests


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe("laboratorium/lab1/auth/rfid")
    # mqtt.publish('laboratorium/lab1/auth/response', {'top_line': 'Connection', 'bottom_line': 'established'})
    data = {"top_line": "Connection", "bottom_line": "established"}
    # mqtt.publish('laboratorium/lab1/auth/response', json.dumps(data))
    print("-" * 20)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    # app.logger.info(buf)
    print(buf)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = json.loads(message.payload.decode())
    user = User.User(payload)

    device_uuid = payload["device_uuid"]

    lab = mongo_functions.get_lab_by_device(device_uuid)
    lab_uuid = lab.get("_id")

    # Check if there are waiting tasks to be performed e.g. a tag assignment
    if queue:
        # Call the corresponding function
        func, data = queue.pop(0)
        res = func(user=data, tag_uuid=payload["tag_uuid"][0])
        print(res)
    else:
        # If there are no tasks in queue

        if payload["tag_uuid"][0] == "C9D3A847":
            mongo_functions.remove_all_from_lab()

        if user.user_uuid != "":

            if user.lab_uuid == "0" or user.lab_uuid == "":
                user.checkin(lab_uuid)
            else:
                user.checkout()

            response = {
                "lab_uuid": user.lab_uuid,
                "top_line": "Welcome" if user.lab_uuid != "0" else "Goodbye",
                "bottom_line": "{} {}.".format(user.last_name, user.first_name[0]),
            }
            mqtt.publish("laboratorium/lab1/auth/response", json.dumps(response))
        else:
            response = {
                "lab_uuid": user.lab_uuid,
                "top_line": "Error",
                "bottom_line": "Unknown User",
            }
            mqtt.publish("laboratorium/lab1/auth/response", json.dumps(response))


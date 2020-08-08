from flask import Flask, jsonify, request, current_app
from laboratorium import mongo, User, queue, events
from laboratorium import mongo_functions as mf
from flask_restful import Resource
import json, random, requests, re
from pprint import pprint

mongo_labs = mongo.db["labs"]
mongo_users = mongo.db["users"]


class SlashLab(Resource):
    def post(self):
        payload = {}

        commands = {
            "": status,
            "stats": stats,
            "checkout": checkout,
            "mock": mock,
            "add-tag": add_tag,
            "clear-queue": clear_queue,
            "kick": kick,
        }

        # pprint(request.headers)

        authorized_headers = current_app.config["AUTHORIZED_HEADERS"]

        authorized = False

        for i in request.headers:
            if i[0] == "Authorization":
                if i[1][6:] in authorized_headers:
                    authorized = True

        if authorized:
            message = request.form["text"]
            command = message.split()[0] if message != "" else ""
            data = message[(len(command) if len(command) == 0 else len(command) + 1) :]

            func = commands.get(command)
            if func is None:
                return jsonify(response_format("This command does not exist.", "!"))
            payload = func(data)
            return jsonify(payload)
        else:
            return "Not authorized"


def response_format(text, image_format="HI"):
    return {
        "text": text,
        "username": "Laboratorium",
        "icon_url": "https://eu.ui-avatars.com/api/?name={}".format(image_format),
    }


def status(data):
    for lab in mongo_labs.find():
        # mongo_labs.update({'_id': 'lab1'}, {'$inc': {'user_count': 1}})
        users = lab["users"]
        if len(users) == 1:
            message = f"There is 1 user in {lab['desc']}\n\n"
        else:
            message = f"There are {len(users)} users in {lab['desc']}\n\n"
        for user in users:
            # print("user:", user)
            # user = mongo_users.find_one({"_id": user})
            user = User.User({"_id": user})
            message += f"{user.first_name} {user.last_name}\n"
        return response_format(message, len(users))


def stats(data):
    lab = mongo_labs.find_one({"_id": "lab1"})
    return response_format(
        "The lab statistics for today! {}, {}".format(lab["user_count"], lab["_id"]),
        request.form["user_name"],
    )


def checkout(data):
    mm_username = request.form["user_name"]
    user = User.User({"mm_username": mm_username})
    lab = mongo_labs.find_one({"_id": user.lab_uuid})

    if user.lab_uuid != "0":
        user.checkout()
        text = "The user {} was successfully checked out!".format(user.mm_username)
        payload = response_format(text, user.first_name)
    else:
        payload = response_format("You are not checked in any lab!", user.first_name)
    return payload


def mock(data):
    ans = []
    for c in data:
        ans.append(c.upper() if random.randint(0, 1) == 1 else c.lower())
    return response_format("".join(ans), "M")


def add_tag(data):
    data = data.split(" ", 1)

    # ! Care when using in async
    if hook_user_is_admin():
        text = "You are not allowed to excecute this command."
    elif len(data) == 1:
        username = data[0]
        user = User.User({"mm_username": username})
        print(username, user.__dict__)
        if user.user_uuid != "":
            # Add the new assignment task in queue
            queue.append((events.add_tag_after_command, user))
            text = "Waiting for tag scan..."
        else:
            text = "User does not exist."
    else:
        text = "Wrong request format."

    return response_format(text, text)


def clear_queue(data):
    queue.clear()
    return response_format("Queue was cleared successfully.")


def kick(data):
    if hook_user_is_admin():
        if "all" in data:
            mf.remove_all_from_lab()
            return response_format("Users have been kicked.")
        else:
            return response_format("Invalid kick method.")
    else:
        return response_format("You are not an administrator.")


def hook_user_is_admin():
    hook_user = User.User({"mm_username": request.form.get("user_name")})
    return hook_user.administrator

from flask import Flask, jsonify, request, current_app
from laboratorium import mongo, User, queue, events
from laboratorium import mongo_functions as mf
from flask_restful import Resource
import json, random, requests, re

mongo_labs = mongo.db["labs"]
mongo_users = mongo.db["users"]


class SlashLab(Resource):
    def post(self):
        payload = {}

        cases = {
            "": status,
            "stats": stats,
            "checkout": checkout,
            "mock": mock,
            "add-tag": add_tag,
            "clear-queue": clear_queue,
        }

        message = request.form["text"]
        command = message.split()[0] if message != "" else ""
        data = message[(len(command) if len(command) == 0 else len(command) + 1) :]

        func = cases.get(command)
        payload = func(data)
        return jsonify(payload)


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
        payload = {
            "text": message,
            "username": "Lab Authenticator",
            "icon_url": "https://eu.ui-avatars.com/api/?name={}".format(len(users)),
        }
        return payload


def stats(data):
    lab = mongo_labs.find_one({"_id": "lab1"})
    payload = {
        "text": "The lab statistics for today! {}, {}".format(
            lab["user_count"], lab["_id"]
        ),
        "username": "Lab Stats",
        "icon_url": "https://eu.ui-avatars.com/api/?name={}".format(
            request.form["user_name"]
        ),
    }
    return payload


def checkout(data):
    mm_username = request.form["user_name"]
    user = User.User({"mm_username": mm_username})
    lab = mongo_labs.find_one({"_id": user.lab_uuid})

    if user.lab_uuid != "0":
        user.checkout()
        payload = {
            "text": "The user {} was successfully checked out!".format(
                user.mm_username
            ),
            "username": "Lab Authenticator",
            "icon_url": "https://eu.ui-avatars.com/api/?name={}".format(
                user.first_name
            ),
        }
    else:
        payload = {
            "text": "You are not checked in any lab!",
            "username": "Lab Authenticator",
            "icon_url": "https://eu.ui-avatars.com/api/?name={}".format(
                user.first_name
            ),
        }
    return payload


def count(data):
    pass


def mock(data):
    ans = []
    for c in data:
        ans.append(c.upper() if random.randint(0, 1) == 1 else c.lower())
    payload = {
        "text": "".join(ans),
        "username": "lAB AutHeNTIcAtOr",
        "icon_url": "https://eu.ui-avatars.com/api/?name={}".format("M"),
    }
    return payload


def add_tag(data):
    data = data.split(" ", 1)
    hook_user = User.User({"mm_username": request.form.get("user_name")})
    if not hook_user.administrator:
        text = "You are not allowed to excecute this command."
    elif len(data) == 1:
        username = data[0]
        user = User.User({"mm_username": username})
        print(username, user.__dict__)
        if user.user_uuid != "":
            # Add the new assignment task in queue
            queue.append((events.add_tag_after_command, user))
            text = "Waiting for tag scan"
        else:
            text = "User does not exist"
    else:
        text = "Wrong request format"

    payload = {
        "text": text,
        "username": "Lab Authenticator",
        "icon_url": "https://eu.ui-avatars.com/api/?name={}".format(text),
    }
    return payload


def clear_queue(data):
    queue.clear()
    return "clear"

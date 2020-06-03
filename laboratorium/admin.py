from flask import request
from flask_restful import Resource
from laboratorium.User import User
from laboratorium import auth

from laboratorium import mongo_functions
from laboratorium import redis_functions

import json


# TODO: delete objects when no longer needed


class GetUser(Resource):
    @auth.login_required
    def get(self, tag_uuid):
        user = User({"tag_uuid": tag_uuid})
        user.init_from_mongo()

        if user.user_uuid is not None:
            # resp = {
            #     "user_uuid": user.user_id,
            #     "secondary_id": user.second_id,
            #     "first_name": user.first_name,
            #     "last_name": user.last_name,
            #     "mm_username": user.mm_username,
            #     "project": user.project,
            # }
            # if user.user_uuid is not None:
            return user.__dict__
        else:
            return {"error": "user not found"}, 409


class AddUser(Resource):
    @auth.login_required
    def put(self):
        user_dict = request.json
        user = User(user_dict)
        return mongo_functions.add_user(user)


class GetUsers(Resource):
    @auth.login_required
    def get(self):
        users = mongo_functions.get_all_users()
        #for user in users:
        #    user.lab_uuid = redis_functions.get_lab_uuid(user)
        return [l.__dict__ for l in users]


class MakeAdministrator(Resource):
    @auth.login_required
    def post(self):
        user = User(request.json)
        mongo_functions.make_administrator(user)


class MakeAlumni(Resource):
    @auth.login_required
    def post(self):
        user = User(request.json)
        mongo_functions.make_alumni(user)


class AddTag(Resource):
    @auth.login_required
    def post(self):
        user = User(request.json)
        mongo_functions.add_tag(user)


class RemoveTag(Resource):
    @auth.login_required
    def post(self):
        user = User(request.json)
        mongo_functions.remove_tag(user)


class ChangeMmUsername(Resource):
    @auth.login_required
    def post(self):
        user = User(request.json)
        mongo_functions.change_mm_username(user)


class CheckIn(Resource):
    @auth.login_required
    def post(self):
        # Only user_id and in_lab is needed here.
        user = User(request.json)
        user.checkin(request.json['lab_uuid'])
        return {"status": "success"}

class RemoveFromLab(Resource):
    @auth.login_required
    def get(self):
        mongo_functions.remove_all_from_lab()
    

class CheckOut(Resource):
    @auth.login_required
    def post(self):
        user = User(request.json)
        user.checkout()
        return {"status": "success"}


class Authenticate(Resource):
    # @auth.login_required
    def post(self):
        user = User(request.json)
        return {"status": user.authenticate()}

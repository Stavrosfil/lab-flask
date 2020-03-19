from flask import request
from flask_restful import Resource

from flask import g, current_app as app
from laboratorium.db import get_db, get_user

import json

todos = {}


class GetUser(Resource):
    def get(self, user_id):
        user = dict(get_user(user_id))

        resp = {
            "user_id": user["user_id"],
            "secondary_id": user["secondary_id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "mm_username": user["mm_username"],
            "project": user["project"],
        }

        return resp

        # return {"first_name": user["first_name"]}


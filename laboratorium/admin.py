from flask import request
from flask_restful import Resource

from flask import g, current_app as app
from laboratorium.db import get_db, get_user, query_db

import json

todos = {}


class GetUser(Resource):
    def get(self, user_id):
        user = get_user(user_id)

        if user is not None:
            resp = {
                "user_id": user["user_id"],
                "secondary_id": user["secondary_id"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "mm_username": user["mm_username"],
                "project": user["project"],
            }

            return resp
        else:
            return {"error": "user not found"}, 404

        # return {"first_name": user["first_name"]}


class AddUser(Resource):
    def put(self):
        sql = """ INSERT INTO users (id,
                                    second_id,
                                    first_name,
                                    last_name,
                                    mm_username,
                                    project)
              VALUES (?,?,?,?,?,?) """

        user = (
            request.json.get("id"),
            request.json.get("second_id"),
            request.json.get("first_name"),
            request.json.get("last_name"),
            request.json.get("mm_username"),
            request.json.get("project"),
        )

        try:
            cur = get_db().cursor()
            cur.execute(sql, user)
            cur.close()
            get_db().commit()
        except Exception as e:
            return str(e), 409

        return cur.lastrowid

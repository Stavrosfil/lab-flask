from flask import request
from flask_restful import Resource
from laboratorium.User import User

from laboratorium.db import get_db, get_user, query_db

import json


class GetUser(Resource):
    def get(self, user_id):
        user = User(get_user(user_id))

        if user.user_id is not None:
            resp = {
                "user_id": user.user_id,
                "secondary_id": user.second_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "mm_username": user.mm_username,
                "project": user.project,
            }

            return resp
        else:
            return {"error": "user not found"}, 404

        # return {"first_name": user["first_name"]}


class AddUser(Resource):
    def put(self):
        sql = """ INSERT INTO users (user_id,
                                    second_id,
                                    first_name,
                                    last_name,
                                    mm_username,
                                    project,
                                    administrator)
              VALUES (?,?,?,?,?,?,?) """

        user = User(request.json)
        sql_data = (
            user.user_id,
            user.second_id,
            user.first_name,
            user.last_name,
            user.mm_username,
            user.project,
            user.administrator,
        )

        try:
            cur = get_db().cursor()
            cur.execute(sql, sql_data)
            cur.close()
            get_db().commit()
        except Exception as e:
            return str(e), 409

        return cur.lastrowid


class GetUsers(Resource):
    def get(self):
        sql = "select * from users"
        q = query_db(sql)

        resp = []
        for user in q:
            user = User(dict(user))
            resp.append(user.__dict__)

        return resp

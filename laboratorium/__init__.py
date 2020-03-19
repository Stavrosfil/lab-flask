import os

from . import db

from flask import Flask, g, request
from flask_redis import FlaskRedis
from flask_restful import Resource, Api
import laboratorium.admin
import sqlite3

r = FlaskRedis()


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Load app config file
    # app.config.from_envvar('APP_CONFIG')
    app.config.from_pyfile("config.py", silent=False)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize global objects
    r.init_app(app)
    api = Api(app)

    api.add_resource(admin.GetUser, "/admin/getuser/<string:user_id>")
    api.add_resource(admin.AddUser, "/admin/adduser")

    with app.app_context():

        db.init_app()

        #     from . import auth
        #     app.register_blueprint(auth.bp)

        return app

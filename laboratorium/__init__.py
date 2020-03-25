import os
from flask import Flask, g, request
from flask_redis import FlaskRedis
from flask_restful import Resource, Api
from flask_influxdb import InfluxDB
from flask_pymongo import PyMongo
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from laboratorium import routes

r = FlaskRedis()
influx = InfluxDB()
mongo = PyMongo()
auth = HTTPBasicAuth()
users = {}


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Load app config file
    app.config.from_pyfile("config.py", silent=False)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():

        users.update({
            app.config["ADMIN"]:
            generate_password_hash(app.config["ADMIN_PW"]),
        })

        # Initialize global objects
        r.init_app(app)
        influx.init_app(app)
        api = Api(app)
        mongo.init_app(app, app.config["MONGO_URI"])

        routes.init_routes(api)

        return app


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False
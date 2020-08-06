import os

from flask import Flask, g, request
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from flask_httpauth import HTTPBasicAuth
from flask_mqtt import Mqtt
from influxdb import InfluxDBClient
import paho.mqtt.client as mqttr
from werkzeug.security import generate_password_hash, check_password_hash

from laboratorium import routes

influx = InfluxDBClient("influxdb", 8086, "root", "root", "lab_users")
mongo = PyMongo()
auth = HTTPBasicAuth()
mqtt = Mqtt()
users = {}
queue = []


def create_app():
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

        users.update(
            {app.config["ADMIN"]: generate_password_hash(app.config["ADMIN_PW"]),}
        )

        # Initialize global objects
        mongo.init_app(app)
        mqtt.client_id = app.config["MQTT_CLIENT_ID"]
        mqtt.init_app(app)

        from . import mqtt_functions

        mqtt_functions

        api = Api(app)
        routes.init_routes(api)

        return app


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


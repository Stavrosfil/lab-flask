import os
from . import db
from flask import Flask, g, request
from flask_redis import FlaskRedis
from flask_restful import Resource, Api
from laboratorium import routes
from flask_influxdb import InfluxDB


r = FlaskRedis()
influx = InfluxDB()


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
        # Initialize global objects
        r.init_app(app)
        influx.init_app(app)

        api = Api(app)
        routes.init_routes(api)

        db.init_app()

        return app

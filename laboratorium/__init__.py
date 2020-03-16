import os

from flask import Flask, g
from flask_redis import FlaskRedis


r = FlaskRedis()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # app.config.from_envvar('APP_CONFIG')
    app.config.from_pyfile('config.py', silent=False)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    r.init_app(app)

    with app.app_context():

        from . import db
        # db.init_app()

        from . import mqtt_handler
        # mqtt_handler.init_mqtt()

        from . import auth
        app.register_blueprint(auth.bp)

        return app

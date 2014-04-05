from flask import Flask
from config import config
from flask.ext.pymongo import PyMongo

mongo = PyMongo()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # intializes plugin(s)
    mongo.init_app(app)

    from app.api_1_0 import appApi
    appApi.init_app(app)

    return app

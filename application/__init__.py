import os
from flask import Flask
from flask_mongoengine import MongoEngine
from celery import Celery

dburl = 'mongodb://127.0.0.1:27017/clickpost'

celery = Celery(__name__, broker='amqp://localhost/')

#Class-based application configuration
class ConfigClass(object):
    """ Flask application settings """

    dburl = 'mongodb://127.0.0.1:27017/clickpost'
    # Flask settings
    SECRET_KEY = 'Whatever just dont use this in production'
    ENV = 'DEVELOPMENT'

    # Flask-Mongoengine settings
    MONGODB_SETTINGS = {
        'db': 'clickpost',
        'host': dburl
    }

def create_app():

    app = Flask(__name__)
    app.config.from_object(__name__ + '.ConfigClass')

    db = MongoEngine(app)

    from .controllers import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
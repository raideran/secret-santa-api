from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
api = Api()
jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    jwt.init_app(app)

    from . import routes
    api.init_app(app)
    from .models import user, event

    return app

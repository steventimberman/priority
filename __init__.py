from flask import Flask
from . import db as mongodb
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from .utils import JSONEncoder
from . import config

def create_app():
    # TODO: from . import models, routes, services
    app = Flask(__name__)

    from .db import mongo
    app.config.from_object(__name__ + ".config.Config")
    mongo.init_app(app)

    from .extensions import (flask_bcrypt, jwt)
    flask_bcrypt.init_app(app)
    jwt.init_app(app)
    app.json_encoder = JSONEncoder

    from . import users
    users.init_app(app)

    from . import goals
    goals.init_app(app)
    # TODO: initialize each folder (models.init_app(app))
    return app

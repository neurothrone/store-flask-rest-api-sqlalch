import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from src.data.constants import DATABASE_PATH
from src.management.database import db
from src.management.security import authenticate, identity

from resources.item import ItemResource, ItemListResource
from resources.store import StoreResource, StoreListResource
from resources.user import UserRegisterResource


if __name__ == "__main__":
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.urandom(24)
    api = Api(app)
    jwt = JWT(app, authenticate, identity)  # creates new endpoint: /auth

    api.add_resource(ItemResource, "/item/<string:name>")
    api.add_resource(ItemListResource, "/items")
    api.add_resource(StoreResource, "/store/<string:name>")
    api.add_resource(StoreListResource, "/stores")
    api.add_resource(UserRegisterResource, "/register")

    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(port=5000, debug=True)

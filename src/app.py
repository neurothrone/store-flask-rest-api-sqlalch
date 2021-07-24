import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from resources.item import ItemResource, ItemListResource
from resources.store import StoreResource, StoreListResource
from resources.user import UserResource, UserLoginResource, UserRegisterResource
from src.management.database import db


DATABASE_PATH = "../data/data.db"

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = os.urandom(24)
api = Api(app)
jwt = JWTManager(app)

api.add_resource(ItemResource, "/item/<string:name>")
api.add_resource(ItemListResource, "/items")
api.add_resource(StoreResource, "/store/<string:name>")
api.add_resource(StoreListResource, "/stores")
api.add_resource(UserResource, "/user/<int:user_id>")
api.add_resource(UserLoginResource, "/login")
api.add_resource(UserRegisterResource, "/register")


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000)

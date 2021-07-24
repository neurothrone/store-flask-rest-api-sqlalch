from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required)
from flask_restful import reqparse
from werkzeug.security import safe_str_cmp

from src.models.user import UserModel
from src.resources.base import BaseResource

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username",
                          type=str,
                          required=True,
                          help="Username field cannot be blank")
_user_parser.add_argument("password",
                          type=str,
                          required=True,
                          help="Password field cannot be blank")


class UserResource(BaseResource):
    parser = reqparse.RequestParser()
    parser.add_argument("user_id",
                        type=str,
                        required=True,
                        help="User id field cannot be blank")

    @classmethod
    @jwt_required()
    def get(cls, user_id: int) -> tuple[dict, int]:
        try:
            if user := UserModel.find_by_id(user_id):
                return user.to_json(), 200
        except:
            return cls.response(
                message="An error occured requesting the user.",
                status_code=500)
        return cls.response(
            message=f"There is no user with the user id '{user_id}'.",
            status_code=404)

    @classmethod
    @jwt_required()
    def delete(cls, user_id: int) -> tuple[dict, int]:
        if user := UserModel.find_by_id(user_id):
            try:
                user.delete_from_db()

                return cls.response(
                    message="User deleted.",
                    status_code=200,
                    name=user.username)
            except:
                return cls.response(
                    message="An error occurred deleting the user.",
                    status_code=500)
        return cls.response(
            message=f"There is no user with the user id '{user_id}'.",
            status_code=404)


class UserLoginResource(BaseResource):
    @classmethod
    def post(cls):
        args = _user_parser.parse_args()
        username, password = args["username"], args["password"]

        if (user := UserModel.find_by_username(username)) is None:
            return cls.response(message="Username not found.",
                                status_code=401,
                                name=username)

        if not safe_str_cmp(user.password, password):
            return cls.response(message="Invalid credentials.",
                                status_code=401)

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return {
                   "access_token": access_token,
                   "refresh_token": refresh_token
               }, 200


class UserRegisterResource(BaseResource):
    @classmethod
    def post(cls) -> tuple[dict, int]:
        args = _user_parser.parse_args()
        if not args["username"] or not args["password"]:
            return {"message": "Failed to register, username or password is empty."}, 400

        if UserModel.find_by_username(args["username"]):
            return {"message": "Failed to register, username is taken."}, 400

        user = UserModel(**args)
        user.save_to_db()
        return {"message": "User created successfully."}, 201

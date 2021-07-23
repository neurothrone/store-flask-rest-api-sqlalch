from flask_restful import reqparse

from src.models.user import UserModel
from src.resources.base import BaseResource


class UserRegisterResource(BaseResource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="Username field cannot be blank")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="Password field cannot be blank")

    def post(self) -> tuple[dict, int]:
        args = UserRegisterResource.parser.parse_args()
        if not args["username"] or not args["password"]:
            return {"message": "Failed to register, username or password is empty."}, 400

        if UserModel.find_by_username(args["username"]):
            return {"message": "Failed to register, username is taken."}, 400

        user = UserModel(**args)
        user.save_to_db()
        return {"message": "User created successfully."}, 201


class UserResource(BaseResource):
    parser = reqparse.RequestParser()
    parser.add_argument("user_id",
                        type=str,
                        required=True,
                        help="User id field cannot be blank")

    @classmethod
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

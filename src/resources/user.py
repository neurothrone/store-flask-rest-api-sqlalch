from flask_jwt import jwt_required
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


class UserDeleteResource(BaseResource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="Username field cannot be blank")

    @jwt_required()
    def delete(self, username: str) -> tuple[dict, int]:
        if not username:
            return self.response(
                message="Failed to delete user, username field is missing.",
                status_code=400)

        if user := UserModel.find_by_username(username):
            try:
                user.delete_from_db()

                return self.response(
                    message="User deleted.",
                    status_code=200,
                    name=user.username)
            except:
                return self.response(
                    message="An error occurred deleting the user.",
                    status_code=500)
        return self.response(
            message=f"There is no user by the username '{username}'.",
            status_code=404)

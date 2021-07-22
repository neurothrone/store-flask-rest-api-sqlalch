from flask_restful import Resource, reqparse

from src.models.user import UserModel


class UserRegisterResource(Resource):
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

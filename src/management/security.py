from src.models.user import UserModel


def authenticate(username: str, password: str) -> UserModel or None:
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user
    return None


def identity(payload) -> UserModel or None:
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)

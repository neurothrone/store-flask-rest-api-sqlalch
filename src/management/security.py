from werkzeug.security import safe_str_cmp

from src.models.user import UserModel


def authenticate(username: str, password: str) -> UserModel or None:
    if (user := UserModel.find_by_username(username)) is None or \
            not safe_str_cmp(user.password, password):
        return None
    return user


def identity(payload) -> UserModel or None:
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)

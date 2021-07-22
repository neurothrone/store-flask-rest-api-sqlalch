from src.management.database import db

from src.models.base import BaseModel


class UserModel(db.Model, BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def to_json(self) -> dict:
        return {"user": self.username}

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: str) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

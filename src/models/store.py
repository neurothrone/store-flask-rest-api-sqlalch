from src.management.database import db

from src.models.base import BaseModel


class StoreModel(db.Model, BaseModel):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name: str) -> None:
        self.name = name

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.to_json() for item in self.items.all()]
        }

    @classmethod
    def all_to_json(cls) -> list[dict]:
        return [item.to_json() for item in cls.find_all()]

    @classmethod
    def find_by_name(cls, name: str) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: str) -> "StoreModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> list["StoreModel"]:
        return cls.query.all()

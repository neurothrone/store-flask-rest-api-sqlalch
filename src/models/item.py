from src.management.database import db

from src.models.base import BaseModel


class ItemModel(db.Model, BaseModel):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name: str, price: float, store_id: int) -> None:
        self.name = name
        self.price = price
        self.store_id = store_id

    def update(self, new_price: float) -> None:
        self.price = new_price
        self.save_to_db()

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id
        }

    @classmethod
    def all_to_json(cls) -> list[dict]:
        return [item.to_json() for item in cls.find_all()]

    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> list["ItemModel"]:
        return cls.query.all()



from src.management.database import db


class ItemModel(db.Model):
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

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self, new_price) -> None:
        self.price = new_price
        self.save_to_db()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> list["ItemModel"]:
        return cls.query.all()

    @classmethod
    def all_to_json(cls) -> list[dict]:
        # return list(map(lambda x: x.to_json(), cls.find_all()))
        return [item.to_json() for item in cls.find_all()]

from src.management.database import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name) -> None:
        self.name = name

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.to_json() for item in self.items.all()]
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "StoreModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> list["StoreModel"]:
        return cls.query.all()

    @classmethod
    def all_to_json(cls) -> list[dict]:
        return [item.to_json() for item in cls.find_all()]

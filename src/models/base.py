from src.management.database import db


class BaseModel(db.Model):
    def to_json(self) -> dict:
        pass

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name) -> "BaseModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> list["BaseModel"]:
        return cls.query.all()

    @classmethod
    def all_to_json(cls) -> list[dict]:
        return [cls.to_json() for cls in cls.find_all()]

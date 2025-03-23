import sqlalchemy

from app import db

class BaseRepository:

    model = None

    @classmethod
    def get_all(cls):
        try:
            return cls.model.query.order_by(cls.model.name).all()
        except  sqlalchemy.exc.ArgumentError:
            return cls.model.query.all()

    @classmethod
    def get_by_id(cls, obj_id: int):
        return cls.model.query.get(obj_id)

    @classmethod
    def create(cls, obj):
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def delete(cls, obj):
        db.session.delete(obj)
        db.session.commit()

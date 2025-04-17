import sqlalchemy

from app import db

class BaseRepository:
    """Classe de base pour les opérations CRUD sur un modèle SQLAlchemy."""

    model = None

    @classmethod
    def get_all(cls):
        """Récupère tous les objets du modèle, triés par nom si possible."""
        try:
            return cls.model.query.order_by(cls.model.name).all()
        except sqlalchemy.exc.ArgumentError:
            return cls.model.query.all()

    @classmethod
    def get_by_id(cls, obj_id: int):
        """Récupère un objet du modèle par son identifiant."""
        return db.session.get(cls.model, obj_id)

    @classmethod
    def create(cls, obj):
        """Ajoute un nouvel objet en base de données."""
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def delete(cls, obj):
        """Supprime un objet existant de la base de données."""
        db.session.delete(obj)
        db.session.commit()

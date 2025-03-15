from app.database.tables import db

from .tables import db

def init_db(app):
    """Crée la base de données et les tables si elles n'existent pas encore."""
    with app.app_context():
        db.create_all()
        print("Base de données initialisée avec succès !")

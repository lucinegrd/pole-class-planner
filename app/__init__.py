from flask import Flask
from app.routes import register_routes
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object("config.Config")

    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("Base de données initialisée avec succès !")

    register_routes(app)

    return app

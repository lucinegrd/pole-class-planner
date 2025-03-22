from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name=None):
    app = Flask(__name__, template_folder="templates")

    # Config dynamique
    if config_name == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("Base de données initialisée avec succès !")

    from app.routes import register_routes
    register_routes(app)

    return app

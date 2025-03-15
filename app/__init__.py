from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object("config.Config")

    db.init_app(app)

    # Importer et enregistrer les Blueprints
    from app.routes.eleves import eleves_bp
    app.register_blueprint(eleves_bp)

    return app

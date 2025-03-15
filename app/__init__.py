from flask import Flask
from app.database.tables import db
from app.routes import register_routes

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object("config.Config")

    db.init_app(app)

    register_routes(app)

    return app

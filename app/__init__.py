from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(config_name=None):
    app = Flask(__name__, template_folder="templates")
    app.secret_key="1f87be44cb385f8f7c64a3c98912d6446bcbc05f49f1b6e328e628f309f07437"
    # Config dynamique
    if config_name == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    db.init_app(app)
    with app.app_context():
        from app.models import Course, CourseType, Level, Room, Teacher, Student
        db.create_all()
        print("Base de données initialisée avec succès !")

    from app.routes import register_routes
    register_routes(app)

    return app

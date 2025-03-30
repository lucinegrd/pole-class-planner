from flask import Blueprint

from app.routes.courses import courses_bp
from app.routes.students import students_bp
from app.routes.main import main_bp

def register_routes(app):
    """Enregistre toutes les routes de l'application."""
    app.register_blueprint(students_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(courses_bp)
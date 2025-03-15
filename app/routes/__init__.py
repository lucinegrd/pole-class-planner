from flask import Blueprint
from app.routes.students import students_bp

def register_routes(app):
    """Enregistre toutes les routes de l'application."""
    app.register_blueprint(students_bp)

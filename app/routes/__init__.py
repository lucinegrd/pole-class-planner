from flask import Blueprint

from app.routes.courses_routes import courses_bp
from app.routes.courses_types_routes import course_type_bp
from app.routes.levels_routes import level_bp
from app.routes.rooms_routes import room_bp
from app.routes.students_routes import students_bp
from app.routes.main_routes import main_bp
from app.routes.teachers_routes import teachers_bp
from app.routes.auth import auth_bp

def register_routes(app):
    """Enregistre toutes les routes de l'application."""
    app.register_blueprint(students_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(course_type_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(level_bp)
    app.register_blueprint(auth_bp)
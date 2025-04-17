from app.models import Teacher
from app import db
from app.repositories.base_repository import BaseRepository

class TeacherRepository(BaseRepository):
    """Opérations en base de données pour les professeurs."""

    model = Teacher

    @staticmethod
    def get_by_email(email: str):
        """Récupère un professeur par son adresse email."""
        return Teacher.query.filter_by(email=email).first()

    @staticmethod
    def edit_teacher(teacher: Teacher, first_name: str, last_name: str, email: str):
        """Modifie les informations d'un professeur existant."""
        teacher.first_name = first_name or teacher.first_name
        teacher.last_name = last_name or teacher.last_name
        teacher.email = email or teacher.email
        db.session.commit()

from app.models import Student
from app.repositories.base_repository import BaseRepository

class StudentRepository(BaseRepository):
    """Opérations en base de données pour les étudiants."""

    model = Student

    @staticmethod
    def get_by_email(email: str):
        """Récupère un étudiant par son adresse email"""
        return Student.query.filter_by(email=email).first()

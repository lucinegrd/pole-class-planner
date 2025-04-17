from app.models import Student
from app.repositories.base_repository import BaseRepository
from app import db

class StudentRepository(BaseRepository):
    """Opérations en base de données pour les étudiants."""

    model = Student

    @staticmethod
    def get_by_email(email: str):
        """Récupère un étudiant par son adresse email."""
        return Student.query.filter_by(email=email).first()

    @staticmethod
    def create_student(name, email, credit_balance=0):
        """Crée un nouvel étudiant avec un solde de crédits initial."""
        student = Student(name=name, email=email, credit_balance=credit_balance)
        db.session.add(student)
        db.session.commit()
        return student

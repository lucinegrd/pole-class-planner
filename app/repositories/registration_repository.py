from app import db
from app.models import Registration
from app.repositories.base_repository import BaseRepository

class RegistrationRepository(BaseRepository):
    """Opérations sur les inscriptions aux cours dans la base de données."""

    model = Registration

    @classmethod
    def get_by_course_and_student(cls, course_id: int, student_id: int):
        """Récupère une inscription spécifique selon l'élève et le cours."""
        return Registration.query.filter_by(course_id=course_id, student_id=student_id).first()

    @classmethod
    def get_by_course(cls, course_id: int):
        """Récupère toutes les inscriptions pour un cours donné."""
        return Registration.query.filter_by(course_id=course_id).all()

    @classmethod
    def get_by_student(cls, student_id: int):
        """Récupère toutes les inscriptions d'un élève donné."""
        return Registration.query.filter_by(student_id=student_id).all()

    @classmethod
    def get_by_state(cls, state: str):
        """Récupère toutes les inscriptions selon leur état."""
        return Registration.query.filter_by(state=state).all()

    @classmethod
    def update_state(cls, registration, new_state: str):
        """Met à jour l'état d'une inscription."""
        registration.state = new_state
        db.session.commit()

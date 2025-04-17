from app import db
from app.models import Registration
from app.repositories.base_repository import BaseRepository

class RegistrationRepository(BaseRepository):
    model = Registration

    @classmethod
    def get_by_course_and_student(cls, course_id: int, student_id: int):
        return Registration.query.filter_by(course_id=course_id, student_id=student_id).first()

    @classmethod
    def get_by_course(cls, course_id: int):
        return Registration.query.filter_by(course_id=course_id).all()

    @classmethod
    def get_by_student(cls, student_id: int):
        return Registration.query.filter_by(student_id=student_id).all()

    @classmethod
    def get_by_state(cls, state: str):
        return Registration.query.filter_by(state=state).all()

    @classmethod
    def update_state(cls, registration, new_state: str):
        registration.state = new_state
        db.session.commit()

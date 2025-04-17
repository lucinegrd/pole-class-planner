from app.models import Teacher
from app import db
from app.repositories.base_repository import BaseRepository

class TeacherRepository(BaseRepository):
    model = Teacher

    @staticmethod
    def get_by_email(email: str):
        return Teacher.query.filter_by(email=email).first()

    @staticmethod
    def edit_teacher(teacher: Teacher, first_name: str, last_name: str, email: str):
        teacher.first_name = first_name or teacher.first_name
        teacher.last_name = last_name or teacher.last_name
        teacher.email = email or teacher.email
        db.session.commit()

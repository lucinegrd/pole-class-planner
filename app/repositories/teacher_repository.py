from app.models import Teacher
from app import db
from app.repositories.base_repository import BaseRepository


class TeacherRepository(BaseRepository):

    model = Teacher

    @staticmethod
    def get_by_email(email: str):
        return Teacher.query.filter_by(email=email).first()

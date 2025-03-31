from app.models import Teacher
from app import db
from app.repositories.base_repository import BaseRepository


class TeacherRepository(BaseRepository):

    model = Teacher

    @staticmethod
    def get_by_email(email: str):
        return Teacher.query.filter_by(email=email).first()

    @staticmethod
    def edit_teacher(teacher: Teacher, first_name="", last_name="", email=""):
        if first_name != "" :
            teacher.first_name = first_name
        if last_name != "" :
            teacher.last_name = last_name
        if email != "":
            teacher.email = email
        db.session.commit()

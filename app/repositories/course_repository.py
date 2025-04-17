from datetime import datetime

from sqlalchemy.orm import joinedload

from app.models import Course, Level, CourseType, Teacher, Room
from app.repositories.base_repository import BaseRepository


class CourseRepository(BaseRepository):
    """Opérations spécifiques sur les cours dans la base de données."""

    model = Course

    @classmethod
    def get_all(cls):
        """Récupère tous les cours, triés par date."""
        return Course.query.order_by(Course.date).all()

    @staticmethod
    def get_filtered(level_name=None, course_type_name=None, teacher_name=None, room_name=None):
        """Filtre les cours selon le niveau, le type de cours, le professeur ou la salle."""
        query = Course.query

        if level_name:
            query = query.join(Level).filter(Level.name == level_name)

        if course_type_name:
            query = query.join(CourseType).filter(CourseType.name == course_type_name)

        if teacher_name:
            query = query.join(Teacher).filter(Teacher.first_name == teacher_name)

        if room_name:
            query = query.join(Room).filter(Room.name == room_name)

        return query.order_by(Course.date).all()

    @classmethod
    def get_upcoming_courses(cls, today=None, limit=5):
        """Récupère les prochains cours à partir d'aujourd'hui, avec un nombre maximum donné."""
        today = today or datetime.now()
        return cls.model.query \
            .filter(cls.model.date >= today) \
            .options(
            joinedload(cls.model.teacher),
            joinedload(cls.model.level),
            joinedload(cls.model.course_type),
            joinedload(cls.model.room)
        ) \
            .order_by(cls.model.date.asc()) \
            .limit(limit) \
            .all()

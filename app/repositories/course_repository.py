from app.models.course import Course
from app.database.tables import CourseDB
from app.database.database import db

class CourseRepository:
    @staticmethod
    def get_by_id(course_id):
        """Récupère un cours en base et le convertit en objet métier."""
        db_course = CourseDB.query.get(course_id)
        return Course.from_db(db_course) if db_course else None

    @staticmethod
    def get_all():
        """Récupère tous les cours et les convertit en objets métier."""
        db_courses = CourseDB.query.all()
        return [Course.from_db(cours) for cours in db_courses]

    @staticmethod
    def add(course):
        """Ajoute un cours en base à partir d'un objet Course."""
        db_course = course.to_db()
        db.session.add(db_course)
        db.session.commit()
        return Course.from_db(db_course)

    @staticmethod
    def delete(course_id):
        """Supprime un cours par son ID."""
        course = CourseDB.query.get(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
            return True
        return False

    @staticmethod
    def update(course):
        """Met à jour un cours"""
        db_course = course.to_db()
        db.session.merge(db_course)
        db.session.commit()

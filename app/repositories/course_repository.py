from app import db
from app.models import Course, Student, Level, CourseType, Teacher, Room
from app.repositories.base_repository import BaseRepository


class CourseRepository(BaseRepository):
    """Opération de bas niveau avec la base de données"""

    model = Course

    @classmethod
    def get_all(cls):
        return Course.query.order_by(Course.date).all()

    @staticmethod
    def add_student(course: Course, student: Student):
        if student not in course.students and not course.is_full:
            course.students.append(student)
            db.session.commit()
            return True
        return False  # déjà inscrit ou cours complet

    @staticmethod
    def add_to_waiting_list(course: Course, student: Student):
        if student not in course.waiting_list:
            course.waiting_list.append(student)
            db.session.commit()
            return True
        return False  # déjà en liste d’attente

    @staticmethod
    def remove_student(course: Course, student: Student):
        if student in course.students:
            course.students.remove(student)
            db.session.commit()
            return True
        return False

    @staticmethod
    def remove_from_waiting_list(course: Course, student: Student):
        if student in course.waiting_list:
            course.waiting_list.remove(student)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_filtered(level_name=None, course_type_name=None, teacher_name=None, room_name=None):
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

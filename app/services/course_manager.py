from app.models import Course
from app.repositories.course_repository import CourseRepository
from app.repositories.course_type_repository import CourseTypeRepository
from app.repositories.level_repository import LevelRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.teacher_repository import TeacherRepository
from datetime import datetime

class CourseManager:
    @staticmethod
    def get_course_by_id(course_id):
        """Récupère un cours en utilisant le repository"""
        return CourseRepository.get_by_id(course_id)

    @staticmethod
    def get_all_courses():
        """Récupère tous les cours"""
        return CourseRepository.get_all()


    @staticmethod
    def create_from_form(form_data):
        """
        form_data : un dict (ex: request.form.to_dict())
        Attend les clés : teacher_id, level_id, date, room_id, course_type_id
        """
        course = Course(
            teacher=TeacherRepository.get_by_id(int(form_data['teacher_id'])),
            level=LevelRepository.get_by_id(int(form_data['level_id'])),
            date=datetime.strptime(form_data['date'], "%Y-%m-%dT%H:%M"),
            room=RoomRepository.get_by_id(int(form_data['room_id'])),
            course_type=CourseTypeRepository.get_by_id(int(form_data['course_type_id']))
        )

        CourseRepository.create(course)

        return course

    @staticmethod
    def get_filtered_courses(filters: dict):
        return CourseRepository.get_filtered(
            level_name=filters.get("level"),
            course_type_name=filters.get("type"),
            teacher_name=filters.get("teacher"),
            room_name=filters.get("room")
        )

    @staticmethod
    def add_student_to_course(course_id, student):
        """
        Tente d'ajouter un étudiant à un cours.
        """
        course = CourseRepository.get_by_id(course_id)
        if not course:
            return "not_found"

        if student in course.students:
            return "already_registered"

        if CourseRepository.add_student(course, student):
            return "added"
        if CourseRepository.add_to_waiting_list(course, student):
            return "waiting_list"
        return "already_in_waiting_list"



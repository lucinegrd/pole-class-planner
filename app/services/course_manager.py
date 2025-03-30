from app.models import Course, CourseType
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
    def create_from_form(form):
        """
        form_data : un formulaire
        Attend les clés : teacher_id, level_id, date, room_id, course_type_id
        """
        # Si le type est "autre", créer un nouveau CourseType
        if form.get("course_type") == "autre":
            new_type = CourseType(
                name=form.get("custom_name"),
                description=form.get("custom_description"),
                duration=int(form.get("custom_duration")),
                credit=int(form.get("custom_credit")),
                places=int(form.get("custom_places"))
            )
            CourseTypeRepository.create(new_type)
            course_type_id = new_type.id
        else:
            course_type_id = int(form.get("course_type"))

        date_obj = datetime.strptime(form.get("datetime"), "%Y-%m-%d %H:%M")

        course = Course(
            id_teacher=int(form.get("teacher")),
            id_level=int(form.get("level")),
            date=date_obj,
            id_room=int(form.get("room")),
            id_course_type=course_type_id
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



from app.models import Course, CourseType, Registration
from app.repositories.course_repository import CourseRepository
from app.repositories.course_type_repository import CourseTypeRepository
from app.repositories.registration_repository import RegistrationRepository
from datetime import datetime

from app.services.states.registration_state_base import RegistrationState


class CourseManager:
    """Service pour gérer les opérations sur les cours."""

    @staticmethod
    def get_course_by_id(course_id):
        """Récupère un cours par son identifiant."""
        return CourseRepository.get_by_id(course_id)

    @staticmethod
    def get_all_courses():
        """Récupère tous les cours."""
        return CourseRepository.get_all()

    @staticmethod
    def create_from_form(form):
        """
        Crée un nouveau cours à partir d'un formulaire.

        Paramètre attendu :
        - teacher_id, level_id, date, room_id, course_type_id, ou champs personnalisés si 'autre' est choisi.
        """
        if form.get("course_type") == "autre":
            new_type = CourseType(
                name=form.get("custom_name"),
                description=form.get("custom_description"),
                duration=int(form.get("custom_duration")),
                credit=int(form.get("custom_credit")),
                places=int(form.get("custom_places")),
                color=form.get("custom_color")
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
        """Filtre les cours selon les critères donnés."""
        return CourseRepository.get_filtered(
            level_name=filters.get("level"),
            course_type_name=filters.get("type"),
            teacher_name=filters.get("teacher"),
            room_name=filters.get("room")
        )

    @staticmethod
    def add_student(course, student):
        """Ajoute un élève à un cours en vérifiant la disponibilité."""
        existing = RegistrationRepository.get_by_course_and_student(course_id=course.id, student_id=student.id)
        if existing:
            raise ValueError("Élève déjà inscrit à ce cours.")

        state = "Sur liste d'attente" if course.places <= 0 else "Non validé"

        registration = Registration(course=course, student=student, state=state)
        RegistrationRepository.create(registration)

        RegistrationState.get_state_instance(registration).validate(registration)
        return registration

    @staticmethod
    def confirm_presence(course_id, student_id):
        """Confirme la présence d'un élève à un cours."""
        registration = RegistrationRepository.get_by_course_and_student(course_id, student_id)
        state = RegistrationState.get_state_instance(registration)
        state.complete(registration)
        return registration

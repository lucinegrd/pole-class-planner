from app.repositories.course_repository import CourseRepository
from app.database.tables import CourseDB

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
    def add_course(nom):
        """Crée un cours et le sauvegarde via le repository"""
        new_course = CourseDB(nom=nom)
        return CourseRepository.add(new_course)

    @staticmethod
    def delete_course(course_id):
        """Supprime un cours en passant par le repository"""
        return CourseRepository.delete(course_id)

    @staticmethod
    def add_student_to_course(course_id, student):
        """Ajoute un étudiant à un cours (s’il reste de la place)"""
        course = CourseRepository.get_by_id(course_id)
        if not course:
            return None

        if len(course.students) < course.course_type.places:
            course.students.append(student)
        else:
            course.waiting_list.append(student)

        return CourseRepository.update(course)
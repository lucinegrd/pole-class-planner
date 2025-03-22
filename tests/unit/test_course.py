from app.models import Student, Course, CourseType, Room, Level, Teacher
from datetime import datetime

def test_create_course():
    """
    Test unitaire : création d’un objet Course
    Scénario :
        - Créer un objet Course avec tous les champs requis
    Résultat attendu :
        - L’objet est bien instancié avec les relations associées
    """
    teacher = Teacher(first_name="Emma", last_name="Lemoine", email="emma@example.com", password_hash="hash")
    level = Level(name="Avancé")
    room = Room(name="Studio C")
    course_type = CourseType(name="Pole Strong", description="Renfo & figures", duration=60, credit=1, places=10)

    course = Course(
        teacher=teacher,
        level=level,
        room=room,
        course_type=course_type,
        date=datetime(2025, 4, 5, 19, 0)
    )

    assert course.teacher.first_name == "Emma"
    assert course.level.name == "Avancé"
    assert course.room.name == "Studio C"
    assert course.course_type.name == "Pole Strong"
    assert course.date.year == 2025


def test_is_full_returns_false_when_not_enough_students(sample_course):
    """
    Test unitaire : Course.is_full
    Scénario :
        - Créer un cours avec 3 places
        - Ajouter 2 étudiants
    Résultat attendu :
        - course.is_full doit retourner False
    """
    student1 = Student(name="Lucine Giraud", email="lucine@example.com")
    student2 = Student(name="Angel Ayme", email="angel@example.com")

    sample_course.students.extend([student1, student2])

    assert sample_course.is_full is False

def test_is_full_returns_true_when_students_reach_limit(sample_course):
    """
    Test unitaire : Course.is_full
    Scénario :
        - Créer un cours avec 3 places
        - Ajouter 3 étudiants
    Résultat attendu :
        - course.is_full doit retourner True
    """
    student1 = Student(name="Marie Dubois", email="marie@example.com")
    student2 = Student(name="Léa Morel", email="lea@example.com")
    student3 = Student(name="Noémie Durand", email="noemie@example.com")

    sample_course.students.extend([student1, student2, student3])

    assert sample_course.is_full is True

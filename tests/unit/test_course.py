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



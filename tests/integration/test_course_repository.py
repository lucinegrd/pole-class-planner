import pytest
from datetime import datetime
from app.models import Course, Student, Teacher, Room, CourseType, Level
from app.repositories import CourseRepository, TeacherRepository, CourseTypeRepository, LevelRepository, RoomRepository
from app import db

def test_get_course_by_id(app, sample_course):
    """
    Test d'intégration : CourseRepository.get_by_id
    Scénario :
        - Récupérer un cours existant par son ID
    Résultat attendu :
        - Le bon cours est retourné
    """
    CourseRepository.create(sample_course)
    course = CourseRepository.get_by_id(sample_course.id)
    assert course is not None
    assert course.id == sample_course.id

def test_get_all_courses(app, sample_course):
    """
    Test d'intégration : CourseRepository.get_all
    Scénario :
        - Récupérer tous les cours
    Résultat attendu :
        - La liste contient au moins le cours d'exemple
    """
    CourseRepository.create(sample_course)
    all_courses = CourseRepository.get_all()
    assert len(all_courses) >= 1
    assert sample_course in all_courses


def test_get_filtered_by_level(app):
    """
    Test : get_filtered retourne les bons cours selon le niveau
    """
    level = Level(name="Intermédiaire", color="orange")
    LevelRepository.create(level)

    course = Course(
        teacher=Teacher(first_name="Paul", last_name="Dupont", email="paul@example.com", password_hash="x"),
        level=level,
        room=Room(name="Studio B"),
        course_type=CourseType(name="Pole Strong", description="Intense", duration=60, credit=1, places=10, color="blue"),
        date=datetime(2025, 4, 10, 18, 0)
    )
    CourseRepository.create(course)

    filtered = CourseRepository.get_filtered(level_name="Intermédiaire")
    assert len(filtered) == 1
    assert filtered[0].level.name == "Intermédiaire"
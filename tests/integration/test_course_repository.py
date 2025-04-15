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


def test_add_student_success(app, sample_course):
    """
    Test d'intégration : CourseRepository.add_student
    Scénario :
        - Ajouter un élève à un cours non complet
    Résultat attendu :
        - L'élève est ajouté à la liste des inscrits
    """
    student = Student(name="Alice", email="alice@example.com")
    db.session.add(student)
    db.session.commit()
    CourseRepository.create(sample_course)
    success = CourseRepository.add_student(sample_course, student)
    assert success is True
    assert student in sample_course.students

def test_add_student_fails_if_full(app, sample_course):
    """
    Test : add_student échoue si le cours est plein
    """
    s1 = Student(name="S1", email="s1@example.com")
    s2 = Student(name="S2", email="s2@example.com")
    s3 = Student(name="S3", email="s3@example.com")
    db.session.add_all([s1, s2, s3])
    db.session.commit()
    CourseRepository.create(sample_course)
    CourseRepository.add_student(sample_course, s1)
    CourseRepository.add_student(sample_course, s2)
    result = CourseRepository.add_student(sample_course, s3)

    assert result is False
    assert s3 not in sample_course.students

def test_add_to_waiting_list_success(app, sample_course):
    """
    Test : add_to_waiting_list ajoute bien un élève
    """
    student = Student(name="Tom", email="tom@example.com")
    db.session.add(student)
    db.session.commit()
    CourseRepository.create(sample_course)
    result = CourseRepository.add_to_waiting_list(sample_course, student)
    assert result is True
    assert student in sample_course.waiting_list

def test_add_to_waiting_list_fails_if_already_there(app, sample_course):
    student = Student(name="Tom", email="tom@example.com")
    db.session.add(student)
    db.session.commit()
    CourseRepository.create(sample_course)
    CourseRepository.add_to_waiting_list(sample_course, student)
    result = CourseRepository.add_to_waiting_list(sample_course, student)

    assert result is False

def test_remove_student(app, sample_course):
    student = Student(name="Ana", email="ana@example.com")
    db.session.add(student)
    db.session.commit()
    CourseRepository.create(sample_course)
    CourseRepository.add_student(sample_course, student)
    result = CourseRepository.remove_student(sample_course, student)

    assert result is True
    assert student not in sample_course.students

def test_remove_from_waiting_list(app, sample_course):
    student = Student(name="Eli", email="eli@example.com")
    db.session.add(student)
    db.session.commit()
    CourseRepository.create(sample_course)
    CourseRepository.add_to_waiting_list(sample_course, student)
    result = CourseRepository.remove_from_waiting_list(sample_course, student)

    assert result is True
    assert student not in sample_course.waiting_list

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
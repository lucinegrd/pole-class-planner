from datetime import datetime
from app import db
from app.models import Course, Teacher, Student, Level, Room, CourseType
from app.services import CourseManager


def test_create_from_form(app, form_data):
    course = CourseManager.create_from_form(form_data)

    assert course is not None
    assert course.teacher.email == "paul@example.com"
    assert course.level.name == "Débutant"
    assert course.room.name == "Studio A"
    assert course.course_type.name == "Pole Flow"
    assert course.date == datetime(2025, 4, 1, 18, 0)

def test_add_student_to_course(app, form_data):
    course = CourseManager.create_from_form(form_data)
    student = Student(name="Alice", email="alice@example.com")
    db.session.add(student)
    db.session.commit()

    assert CourseManager.add_student_to_course(course.id, student) == "added"
    assert CourseManager.add_student_to_course(course.id, student) == "already_registered"

def test_add_student_to_course_waiting_list(app, form_data):
    course = CourseManager.create_from_form(form_data)

    s1 = Student(name="S1", email="s1@example.com")
    s2 = Student(name="S2", email="s2@example.com")
    s3 = Student(name="S3", email="s3@example.com")
    db.session.add_all([s1, s2, s3])
    db.session.commit()

    CourseManager.add_student_to_course(course.id, s1)
    CourseManager.add_student_to_course(course.id, s2)
    result = CourseManager.add_student_to_course(course.id, s3)

    assert result == "waiting_list"

def test_add_student_to_course_already_in_waiting_list(app, form_data):
    course = CourseManager.create_from_form(form_data)

    s1 = Student(name="Toto", email="toto@example.com")
    s2 = Student(name="Titi", email="titi@example.com")
    s3 = Student(name="Tata", email="tata@example.com")
    db.session.add_all([s1, s2, s3])
    db.session.commit()

    CourseManager.add_student_to_course(course.id, s1)
    CourseManager.add_student_to_course(course.id, s2)
    CourseManager.add_student_to_course(course.id, s3)
    result = CourseManager.add_student_to_course(course.id, s3)

    assert result == "already_in_waiting_list"

def test_add_student_to_nonexistent_course(app):
    student = Student(name="Ghost", email="ghost@example.com")
    db.session.add(student)
    db.session.commit()

    result = CourseManager.add_student_to_course(course_id=999, student=student)
    assert result == "not_found"

def test_get_filtered_courses_by_level(app):
    level = Level(name="Avancé")
    teacher = Teacher(first_name="Lulu", last_name="Pole", email="lulu@example.com", password_hash="x", role="prof")
    room = Room(name="Studio Z")
    course_type = CourseType(name="Exotic", description="Exotique", duration=60, credit=1, places=10)
    db.session.add_all([level, teacher, room, course_type])
    db.session.commit()

    course = Course(
        id_teacher=teacher.id,
        id_level=level.id,
        id_room=room.id,
        id_course_type=course_type.id,
        date=datetime(2025, 4, 15, 18, 0)
    )
    db.session.add(course)
    db.session.commit()

    results = CourseManager.get_filtered_courses({"level": "Avancé"})
    assert len(results) == 1
    assert results[0].level.name == "Avancé"

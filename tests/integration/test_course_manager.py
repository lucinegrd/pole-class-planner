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


def test_get_filtered_courses_by_level(app):
    level = Level(name="Avancé", color="blue")
    teacher = Teacher(first_name="Lulu", last_name="Pole", email="lulu@example.com", password_hash="x", is_admin=False)
    room = Room(name="Studio Z")
    course_type = CourseType(name="Exotic", description="Exotique", duration=60, credit=1, places=10, color="#C9D4FF")
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

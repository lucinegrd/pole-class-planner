import pytest
from app.models import Course, Teacher, Level, Room, CourseType
from datetime import datetime

def test_post_add_course_success(client, session, login_as_admin, setup_base_entities):
    """
    Test end-to-end : Ajout d'un cours (POST)
    """
    # Récupérer les IDs existants de la base
    teacher_id = setup_base_entities["teacher"].id
    level_id = setup_base_entities["level"].id
    room_id = setup_base_entities["room"].id
    course_type_id = setup_base_entities["course_type"].id

    response = client.post("/courses/form", data={
        "teacher": str(teacher_id),
        "level": str(level_id),
        "room": str(room_id),
        "datetime": "2025-04-20 18:00",
        "course_type": str(course_type_id)
    }, follow_redirects=True)

    # Vérifie que ça redirige bien après ajout
    assert response.status_code == 200

    # Vérifie qu'un cours a été créé en BDD
    course = session.query(Course).filter_by(id_teacher=teacher_id).first()
    assert course is not None
    assert course.level.id == level_id
    assert course.room.id == room_id
    assert course.course_type.id == course_type_id
    assert course.date == datetime(2025, 4, 20, 18, 0)

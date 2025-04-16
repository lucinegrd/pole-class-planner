from app import create_app, db
from app.models import Teacher, Level, Room, CourseType, Course, Student
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    # Création des enseignants
    t1 = Teacher(
        first_name="Lucine",
        last_name="Giraud",
        email="lucine.grd@gmail.com",
        password_hash=generate_password_hash("123"),
        is_admin=True
    )
    t2 = Teacher(
        first_name="Marie",
        last_name="Durand",
        email="marie@example.com",
        password_hash=generate_password_hash("password123"),
        is_admin=False
    )
    t3 = Teacher(
        first_name="Sophie",
        last_name="Martin",
        email="sophie@example.com",
        password_hash=generate_password_hash("password123"),
        is_admin=False
    )

    # Autres entités
    levels = [Level(name=level[0], color=level[1]) for level in [("Débutant", "green"), ("Intermédiaire", "blue"), ("Avancé", "red")]]
    rooms = [Room(name=n) for n in ["Studio A", "Studio B", "Studio C"]]
    course_types = [
        CourseType(name="Pole Dance", description="Cours de pole dance", duration=75, credit=2, places=10, color="violet"),
        CourseType(name="Cerceau", description="Cours de cerceau", duration=60, credit=2, places=8, color="orange")
    ]

    db.session.add_all([t1, t2, t3] + levels + rooms + course_types)
    db.session.commit()

    # Création d'élèves
    students = [
        Student(name="Emma Lopez", email="emma@example.com"),
        Student(name="Clara Moreau", email="clara@example.com"),
        Student(name="Léa Dubois", email="lea@example.com"),
        Student(name="Inès Petit", email="ines@example.com")
    ]
    db.session.add_all(students)
    db.session.commit()

    # Création de cours
    today = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
    courses = [
        Course(
            id_teacher=t2.id,
            id_room=rooms[0].id,
            id_course_type=course_types[0].id,
            id_level=levels[0].id,
            date=today + timedelta(days=1)
        ),
        Course(
            id_teacher=t3.id,
            id_room=rooms[1].id,
            id_course_type=course_types[1].id,
            id_level=levels[1].id,
            date=today + timedelta(days=2)
        ),
        Course(
            id_teacher=t2.id,
            id_room=rooms[2].id,
            id_course_type=course_types[0].id,
            id_level=levels[2].id,
            date=today + timedelta(days=3)
        )
    ]
    db.session.add_all(courses)
    db.session.commit()

    print("✅ Professeurs, niveaux, salles, types, cours et élèves ajoutés avec succès.")

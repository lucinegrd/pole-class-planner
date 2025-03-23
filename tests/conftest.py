import pytest
from app import create_app, db
from app.models import Course, Teacher, Level, Room, CourseType, Student
from datetime import datetime

@pytest.fixture(scope="function")
def app():
    """
    Initialise l'application Flask pour les tests avec une base en mémoire.
    """
    app = create_app("testing")  # Assure-toi d'avoir une config "testing" dans ton app

    return app

@pytest.fixture(scope="function")
def client(app):
    """
    Fournit un client de test Flask (simule les requêtes HTTP).
    """
    return app.test_client()

@pytest.fixture(scope="function")
def session(app):
    """
    Fournit une session SQLAlchemy propre pour chaque test.
    Gère la création et suppression de la base à chaque test.
    """
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_course():
    """
    Fixture pour créer un cours d'exemple avec :
    - un professeur
    - un niveau "Débutant"
    - une salle
    - un type de cours avec 3 places
    - une date fixe
    """
    teacher = Teacher(first_name="Anna", last_name="Smith", email="anna@example.com", password_hash="hashed")
    level = Level(name="Débutant")
    room = Room(name="Studio A")
    course_type = CourseType(
        name="Pole Flow",
        description="Cours fluide",
        duration=60,
        credit=1,
        places=2
    )


    return Course(
        teacher=teacher,
        level=level,
        room=room,
        date=datetime(2025, 4, 1, 18, 0),
        course_type=course_type
    )

@pytest.fixture
def form_data(app):
    """
    Prépare un dictionnaire simulant des données de formulaire pour la création de cours.
    """
    teacher = Teacher(first_name="Paul", last_name="Prof", email="paul@example.com", password_hash="x")
    level = Level(name="Débutant")
    room = Room(name="Studio A")
    course_type = CourseType(name="Pole Flow", description="Fluidité", duration=60, credit=1, places=2)

    db.session.add_all([teacher, level, room, course_type])
    db.session.commit()

    return {
        "teacher_id": str(teacher.id),
        "level_id": str(level.id),
        "room_id": str(room.id),
        "course_type_id": str(course_type.id),
        "date": "2025-04-01T18:00"
    }

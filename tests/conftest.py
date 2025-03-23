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

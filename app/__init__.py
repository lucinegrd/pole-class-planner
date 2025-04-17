from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

login_manager = LoginManager()
login_manager.login_view = "auth.login"


db = SQLAlchemy()

def create_app(config_name=None):
    app = Flask(__name__, template_folder="templates")
    app.secret_key="1f87be44cb385f8f7c64a3c98912d6446bcbc05f49f1b6e328e628f309f07437"
    # Config dynamique
    if config_name == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        init_db()

    from app.routes import register_routes
    register_routes(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import Teacher
    return db.session.get(Teacher, int(user_id))

def init_db():
    from app.models import Teacher, Level, Room, CourseType, Course, Subscription, Student, Registration
    from app.repositories.registration_repository import RegistrationRepository
    from app.services.states.registration_state_base import RegistrationState
    from datetime import timedelta, datetime
    import random

    db.drop_all()
    db.create_all()

    # Création des enseignants
    t1 = Teacher(first_name="Lucine", last_name="Giraud", email="lucine.grd@gmail.com",
                 password_hash=generate_password_hash("123"), is_admin=True)
    t2 = Teacher(first_name="Marie", last_name="Durand", email="marie@example.com",
                 password_hash=generate_password_hash("password123"), is_admin=False)
    t3 = Teacher(first_name="Sophie", last_name="Martin", email="sophie@example.com",
                 password_hash=generate_password_hash("password123"), is_admin=False)
    db.session.add_all([t1, t2, t3])

    # Création des niveaux
    levels = [
        Level(name="Niv 1", color="#aed498"),
        Level(name="Niv 2", color="#5ff5c8"),
        Level(name="Niv 3", color="#5f7df5")
    ]
    db.session.add_all(levels)

    # Création des salles
    rooms = [Room(name="Studio A"), Room(name="Studio B"), Room(name="Studio C")]
    db.session.add_all(rooms)

    # Création des types de cours (limités à 5-8 places)
    course_types_data = [
        ("Pole Dance", "Cours de pole dance, amenez un short", 75, 2, 6, "#eb8f34"),
        ("Cerceau", "Cours de cerceau, legging recommandé", 60, 2, 7, "#eb34ba"),
        ("Souplesse", "Cours de souplesse", 60, 1, 8, "#34b4eb"),
        ("Renfo", "Renforcement musculaire", 45, 1, 5, "#ffd700"),
        ("Exotic", "Cours exotic heels", 60, 2, 6, "#8e44ad"),
    ]
    course_types = [CourseType(name=name, description=desc, duration=dur, credit=cred, places=plc, color=col) for
                    name, desc, dur, cred, plc, col in course_types_data]
    db.session.add_all(course_types)
    db.session.commit()

    # Création d'élèves avec soit crédits, soit abonnement
    student_names = ["Emma", "Clara", "Léa", "Inès", "Julie", "Anna", "Sophie", "Camille", "Eva", "Chloé", "Manon",
                     "Lucie", "Lucas", "Nathan", "Hugo"]
    students = []
    today = datetime.now()
    for i, name in enumerate(student_names):
        student = Student(name=f"{name} Dupont", email=f"{name.lower()}@example.com")

        has_subscription = random.random() < 0.5
        if has_subscription:
            student.credit_balance = 0
        else:
            student.credit_balance = random.choice([10, 20, 40])

        students.append(student)

    db.session.add_all(students)
    db.session.commit()

    # Ajout d'abonnements seulement aux élèves qui n'ont pas de crédits
    for i, student in enumerate(students):
        if student.credit_balance == 0:
            sub = Subscription(
                student=student,
                start_date=today - timedelta(days=random.randint(1, 10)),
                end_date=today + timedelta(days=random.randint(30, 40)),
                weekly_limit=random.choice([1, 2, 3])
            )
            db.session.add(sub)

    db.session.commit()

    # Génération de 60 cours sur plusieurs semaines (1 à 3 par jour sauf dimanche)
    base_date = today.replace(hour=10, minute=0, second=0, microsecond=0)
    courses = []
    day_offset = 0
    while len(courses) < 60:
        day = base_date + timedelta(days=day_offset)
        if day.weekday() != 6:  # pas de cours le dimanche
            nb_courses_today = random.choice([1, 2, 3])
            hours = random.sample([10, 17, 19], nb_courses_today)
            for hour in hours:
                ctype = random.choice(course_types)
                course = Course(
                    id_teacher=random.choice([t1.id, t2.id, t3.id]),
                    id_room=random.choice(rooms).id,
                    id_course_type=ctype.id,
                    id_level=random.choice(levels).id,
                    date=day.replace(hour=hour)
                )
                courses.append(course)
        day_offset += 1

    db.session.add_all(courses)
    db.session.commit()

    # Inscriptions aléatoires (cohérentes avec crédits et abonnements)
    all_courses = Course.query.all()
    enrolled_students = random.sample(students, 10)
    for student in enrolled_students:
        if student.credit_balance == 0:
            for course in random.sample(all_courses, k=random.randint(1, 4)):
                registration = Registration(course=course, student=student)
                RegistrationRepository.create(registration)
                RegistrationState.get_state_instance(registration).validate(registration)
        else :
            for course in random.sample(all_courses, k=random.randint(5, 10)):
                registration = Registration(course=course, student=student)
                RegistrationRepository.create(registration)
                RegistrationState.get_state_instance(registration).validate(registration)



    db.session.commit()

    print("Base de données initialisée.")
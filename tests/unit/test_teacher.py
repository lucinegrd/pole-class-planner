from app.models import Teacher
import pytest
from app import db

def test_create_teacher():
    """
    Test unitaire : création d'un objet Teacher
    Scénario :
        - Créer un professeur avec tous les champs requis
    Résultat attendu :
        - Les attributs sont correctement enregistrés
    """
    teacher = Teacher(
        first_name="Lucine",
        last_name="Giraud",
        email="lucine@example.com",
        password_hash="hashed_password",
        is_admin=False
    )

    assert teacher.first_name == "Lucine"
    assert teacher.last_name == "Giraud"
    assert teacher.email == "lucine@example.com"
    assert teacher.password_hash == "hashed_password"
    assert teacher.is_admin == False

def test_teacher_is_admin_property():
    """
    Test unitaire : propriété is_admin
    Scénario :
        - Créer un prof avec rôle "admin"
        - Créer un prof avec rôle "prof"
    Résultat attendu :
        - is_admin retourne True pour le premier, False pour le second
    """
    admin = Teacher(first_name="Admin", last_name="One", email="admin@example.com", password_hash="x", is_admin=True)
    prof = Teacher(first_name="Prof", last_name="Two", email="prof@example.com", password_hash="y", is_admin=False)

    assert admin.is_admin is True
    assert prof.is_admin is False

def test_teacher_name_property():
    """
    Test unitaire : propriété name (concat first + last)
    Scénario :
        - Créer un prof avec prénom et nom
    Résultat attendu :
        - La propriété `name` retourne "Prénom Nom"
    """
    teacher = Teacher(first_name="Emma", last_name="Lemoine", email="emma@example.com", password_hash="z")

    assert teacher.name == "Emma Lemoine"

def test_duplicate_teacher_email_raises_error(app):
    """
    Test d'intégration : unicité de l'email
    Scénario :
        - Créer deux enseignants avec le même email
    Résultat attendu :
        - Une erreur d'intégrité est levée lors du commit du second
    """
    teacher1 = Teacher(first_name="A", last_name="B", email="duplicate@example.com", password_hash="x")
    teacher2 = Teacher(first_name="C", last_name="D", email="duplicate@example.com", password_hash="y")

    db.session.add(teacher1)
    db.session.commit()

    db.session.add(teacher2)
    with pytest.raises(Exception):
        db.session.commit()

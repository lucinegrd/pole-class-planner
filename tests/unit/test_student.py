import pytest
from app import db
from app.models import Student

def test_create_student():
    """
    Test unitaire : création d'un objet Student
    Scénario :
        - Créer un étudiant avec un nom et un email
    Résultat attendu :
        - Les attributs `name` et `email` sont correctement enregistrés
    """
    student = Student(name="Lucine Giraud", email="giraud.lucine@gmail.com")

    assert student.name == "Lucine Giraud"
    assert student.email == "giraud.lucine@gmail.com"

def test_duplicate_email_raises_error(app):
    """
    Test d'intégration : unicité de l'email
    Scénario :
        - Créer deux étudiants avec le même email
    Résultat attendu :
        - Une erreur d'intégrité doit être levée
    """
    student1 = Student(name="Lucine Giraud", email="duplicate@example.com")
    student2 = Student(name="Autre Élève", email="duplicate@example.com")

    db.session.add(student1)
    db.session.commit()

    db.session.add(student2)
    with pytest.raises(Exception):
        db.session.commit()

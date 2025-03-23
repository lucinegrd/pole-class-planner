import pytest
from app.models import Student
from app.repositories.student_repository import StudentRepository

def test_create_student_and_get_all(app):
    """
    Test d'intégration : StudentRepository.create + get_all
    Scénario :
        - Créer un étudiant
        - Vérifier qu’il est bien présent dans la liste retournée par get_all()
    Résultat attendu :
        - L’étudiant est retrouvé
    """
    student = Student(name="Lucine", email="lucine@example.com")
    StudentRepository.create(student)

    all_students = StudentRepository.get_all()
    assert len(all_students) == 1
    assert all_students[0].email == "lucine@example.com"

def test_get_student_by_id(app):
    """
    Test d'intégration : StudentRepository.get_by_id
    Scénario :
        - Créer un étudiant
        - Le récupérer via son ID
    Résultat attendu :
        - L’étudiant retourné correspond
    """
    student = Student(name="Alex", email="alex@example.com")
    StudentRepository.create(student)

    retrieved = StudentRepository.get_by_id(student.id)
    assert retrieved is not None
    assert retrieved.name == "Alex"

def test_get_student_by_email(app):
    """
    Test d'intégration : StudentRepository.get_by_email
    Scénario :
        - Créer un étudiant
        - Le récupérer via son email
    Résultat attendu :
        - L’étudiant retourné a le bon nom
    """
    student = Student(name="Marie", email="marie@example.com")
    StudentRepository.create(student)

    found = StudentRepository.get_by_email("marie@example.com")
    assert found is not None
    assert found.name == "Marie"

def test_delete_student(app):
    """
    Test d'intégration : StudentRepository.delete
    Scénario :
        - Créer un étudiant
        - Le supprimer
        - Vérifier qu’il n’est plus dans la liste
    Résultat attendu :
        - L’étudiant n’est plus présent après suppression
    """
    student = Student(name="Noah", email="noah@example.com")
    StudentRepository.create(student)
    StudentRepository.delete(student)

    all_students = StudentRepository.get_all()
    assert student not in all_students

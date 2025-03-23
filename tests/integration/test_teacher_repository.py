import pytest
from app.models import Teacher
from app.repositories.teacher_repository import TeacherRepository

def test_create_teacher_and_get_all(app):
    """
    Test d'intégration : TeacherRepository.create + get_all
    Scénario :
        - Créer un enseignant
        - Vérifier qu'il est récupérable via get_all()
    Résultat attendu :
        - L'enseignant est présent dans la liste retournée
    """
    teacher = Teacher(
        first_name="Lucine",
        last_name="Giraud",
        email="lucine@example.com",
        password_hash="hashed"
    )
    TeacherRepository.create(teacher)

    all_teachers = TeacherRepository.get_all()
    assert len(all_teachers) == 1
    assert all_teachers[0].email == "lucine@example.com"

def test_get_teacher_by_id(app):
    """
    Test d'intégration : TeacherRepository.get_by_id
    Scénario :
        - Créer un enseignant
        - Le récupérer via son ID
    Résultat attendu :
        - L'objet retourné a les bonnes infos
    """
    teacher = Teacher(
        first_name="Anna",
        last_name="Morel",
        email="anna@example.com",
        password_hash="x"
    )
    TeacherRepository.create(teacher)

    retrieved = TeacherRepository.get_by_id(teacher.id)
    assert retrieved is not None
    assert retrieved.first_name == "Anna"

def test_get_teacher_by_email(app):
    """
    Test d'intégration : TeacherRepository.get_by_email
    Scénario :
        - Créer un enseignant
        - Le récupérer par son email
    Résultat attendu :
        - L'objet retourné correspond à l'email donné
    """
    teacher = Teacher(
        first_name="Claire",
        last_name="Durand",
        email="claire@example.com",
        password_hash="z"
    )
    TeacherRepository.create(teacher)

    found = TeacherRepository.get_by_email("claire@example.com")
    assert found is not None
    assert found.first_name == "Claire"

def test_delete_teacher(app):
    """
    Test d'intégration : TeacherRepository.delete
    Scénario :
        - Créer un enseignant
        - Le supprimer
        - Vérifier qu'il n'apparaît plus dans get_all()
    Résultat attendu :
        - La liste retournée est vide après suppression
    """
    teacher = Teacher(
        first_name="Jean",
        last_name="Martin",
        email="jean@example.com",
        password_hash="y"
    )
    TeacherRepository.create(teacher)
    TeacherRepository.delete(teacher)

    all_teachers = TeacherRepository.get_all()
    assert teacher not in all_teachers

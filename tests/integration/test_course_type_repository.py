import pytest
from app.models import CourseType
from app.repositories.course_type_repository import CourseTypeRepository

def test_create_course_type_and_get_all(app):
    """
    Test d'intégration : CourseTypeRepository.create + get_all
    Scénario :
        - Créer un type de cours
        - Vérifier qu'il est récupérable via get_all()
    Résultat attendu :
        - Le type de cours est présent dans la liste retournée
    """
    ct = CourseType(
        name="Exotic",
        description="Style fluide et sensuel",
        duration=60,
        credit=1,
        places=12,
        color="DA12DC"
    )
    CourseTypeRepository.create(ct)

    all_types = CourseTypeRepository.get_all()
    assert len(all_types) == 1
    assert all_types[0].name == "Exotic"

def test_get_course_type_by_id(app):
    """
    Test d'intégration : CourseTypeRepository.get_by_id
    Scénario :
        - Créer un type de cours
        - Le récupérer via son ID
    Résultat attendu :
        - L'objet retourné correspond bien au type créé
    """
    ct = CourseType(
        name="Pole Strong",
        description="Renforcement musculaire",
        duration=60,
        credit=1,
        places=10,
        color="DA12DC"
    )
    CourseTypeRepository.create(ct)

    retrieved = CourseTypeRepository.get_by_id(ct.id)
    assert retrieved is not None
    assert retrieved.name == "Pole Strong"

def test_delete_course_type(app):
    """
    Test d'intégration : CourseTypeRepository.delete
    Scénario :
        - Créer un type de cours
        - Le supprimer
        - Vérifier qu'il n'apparaît plus dans get_all()
    Résultat attendu :
        - Le type de cours n’est plus présent après suppression
    """
    ct = CourseType(
        name="Pole Flow",
        description="Travail sur la fluidité",
        duration=60,
        credit=1,
        places=8,
        color="DA12DC"
    )
    CourseTypeRepository.create(ct)
    CourseTypeRepository.delete(ct)

    all_types = CourseTypeRepository.get_all()
    assert ct not in all_types

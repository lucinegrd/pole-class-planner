from app.models import Level
from app.repositories.level_repository import LevelRepository

def test_create_level_and_get_all(app):
    """
    Test d'intégration : LevelRepository.create + get_all
    Scénario :
        - Créer un niveau
        - Vérifier qu'il est récupérable via get_all()
    Résultat attendu :
        - Le niveau est présent dans la liste retournée
    """
    level = Level(name="Débutant")
    LevelRepository.create(level)

    all_levels = LevelRepository.get_all()
    assert len(all_levels) == 1
    assert all_levels[0].name == "Débutant"

def test_get_level_by_id(app):
    """
    Test d'intégration : LevelRepository.get_by_id
    Scénario :
        - Créer un niveau
        - Le récupérer via son ID
    Résultat attendu :
        - L'objet retourné a le bon nom
    """
    level = Level(name="Intermédiaire")
    LevelRepository.create(level)

    retrieved = LevelRepository.get_by_id(level.id)
    assert retrieved is not None
    assert retrieved.name == "Intermédiaire"

def test_delete_level(app):
    """
    Test d'intégration : LevelRepository.delete
    Scénario :
        - Créer un niveau
        - Le supprimer
        - Vérifier qu'il n'apparaît plus dans get_all()
    Résultat attendu :
        - La liste retournée est vide après suppression
    """
    level = Level(name="Avancé")
    LevelRepository.create(level)

    LevelRepository.delete(level)
    all_levels = LevelRepository.get_all()
    assert level not in all_levels

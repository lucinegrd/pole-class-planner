from app.models import Level

def test_create_level():
    """
    Test unitaire : création d'un objet Level
    Scénario :
        - Créer un objet Level avec un nom
    Résultat attendu :
        - L’attribut `name` est bien enregistré
    """
    level = Level(name="Débutant")

    assert level.name == "Débutant"

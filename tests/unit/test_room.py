from app.models import Room

def test_create_room():
    """
    Test unitaire : création d'un objet Room
    Scénario :
        - Créer une salle avec un nom
    Résultat attendu :
        - L’attribut `name` est bien enregistré
    """
    room = Room(name="Studio A")

    assert room.name == "Studio A"

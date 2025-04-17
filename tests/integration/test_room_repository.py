import pytest
from app.models import Room
from app.repositories.room_repository import RoomRepository

def test_create_room_and_get_all(session):
    """
    Test d'intégration : RoomRepository.create + get_all
    Scénario :
        - Créer une salle
        - Vérifier qu'elle est récupérable via get_all()
    Résultat attendu :
        - La salle est présente dans la liste retournée
    """
    # Nettoyage de la table CourseType
    session.query(Room).delete()
    session.commit()
    room = Room(name="Studio Alpha")
    RoomRepository.create(room)

    all_rooms = RoomRepository.get_all()
    assert len(all_rooms) == 1
    assert all_rooms[0].name == "Studio Alpha"

def test_get_room_by_id(app):
    """
    Test d'intégration : RoomRepository.get_by_id
    Scénario :
        - Créer une salle
        - La récupérer via son ID
    Résultat attendu :
        - L'objet retourné a le bon nom
    """
    room = Room(name="Studio Bêta")
    RoomRepository.create(room)

    retrieved = RoomRepository.get_by_id(room.id)
    assert retrieved is not None
    assert retrieved.name == "Studio Bêta"

def test_delete_room(app):
    """
    Test d'intégration : RoomRepository.delete
    Scénario :
        - Créer une salle
        - La supprimer
        - Vérifier qu'elle n'apparaît plus dans get_all()
    Résultat attendu :
        - La liste retournée est vide après suppression
    """
    room = Room(name="Studio Gamma")
    RoomRepository.create(room)

    RoomRepository.delete(room)
    all_rooms = RoomRepository.get_all()
    assert room not in all_rooms

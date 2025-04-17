from app.models import Room
from app.repositories.base_repository import BaseRepository


class RoomRepository(BaseRepository):
    """Opérations sur les salles dans la base de données."""

    model = Room

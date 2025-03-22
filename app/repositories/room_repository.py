from app.models import Room
from app.repositories.base_repository import BaseRepository


class RoomRepository(BaseRepository):

    model = Room
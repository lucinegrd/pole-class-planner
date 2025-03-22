from app.models import Level
from app.repositories.base_repository import BaseRepository


class LevelRepository(BaseRepository):

    model = Level

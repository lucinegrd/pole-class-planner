from app.models import Level
from app.repositories.base_repository import BaseRepository


class LevelRepository(BaseRepository):
    """Opérations sur les niveaux dans la base de données."""

    model = Level

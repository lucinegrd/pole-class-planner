from app.models import CourseType
from app.repositories.base_repository import BaseRepository


class CourseTypeRepository(BaseRepository):
    """Opérations sur les types de cours dans la base de données."""

    model = CourseType

from app.models import CourseType
from app.repositories.base_repository import BaseRepository


class CourseTypeRepository(BaseRepository):

    model = CourseType

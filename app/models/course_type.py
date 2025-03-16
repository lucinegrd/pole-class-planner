from app.database.tables import CourseTypeDB

class CourseType :
    def __init__(self, name: str, description: str, duration: int, credit: int, places: int):
        self.__name = name
        self.__description = description
        self.__duration = duration
        self.__credit = credit
        self.__places = places

    @property
    def name(self):
        return self.__name
    @property
    def description(self):
        return self.__description
    @property
    def duration(self):
        return self.__duration
    @property
    def credit(self):
        return self.__credit
    @property
    def places(self):
        return self.__places

    @name.setter
    def name(self, value):
        self.__name = value
    @description.setter
    def description(self, value):
        self.__description = value
    @duration.setter
    def duration(self, value):
        self.__duration = value
    @credit.setter
    def credit(self, value):
        self.__credit = value

    @classmethod
    def from_db(cls, db_obj):
        """Transforme un CourseTypeDB en CourseType"""
        return cls(db_obj.name, db_obj.description, db_obj.duration, db_obj.credit, db_obj.places)

    def to_db(self):
        """Transforme un CourseType en CourseTypeDB"""
        return CourseTypeDB(name=self.__name, description=self.__description, duration=self.__duration,
                            credit=self.__credit, places=self.__places)
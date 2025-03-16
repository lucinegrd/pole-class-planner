from app.database.tables import TeacherDB

class Teacher:
    def __init__(self, name:str, email:str):
        self.__name = name
        self.__email = email

    @classmethod
    def from_db(cls, db_obj):
        """Transforme un TeacherDB en Teacher"""
        return cls(db_obj.name, db_obj.email)

    def to_db(self):
        """Transforme un Teacher en TeacherDB"""
        return TeacherDB(name=self.__name, email=self.__email)

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email
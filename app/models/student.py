from app.database.tables import StudentDB

class Student:
    def __init__(self, name, email):
        self.__name = name
        self.__email = email

    @classmethod
    def from_db(cls, db_obj):
        """Transforme un StudentDB en Student"""
        return cls(db_obj.name, db_obj.email)

    def to_db(self):
        """Transforme un Student en StudentDB"""
        return StudentDB(name=self.__name, email=self.__email)


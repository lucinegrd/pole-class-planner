from app import db
from app.database.tables import StudentDB

class Student:
    def __init__(self, name, email):
        self.__name = name
        self.__email = email

    def save_to_db(self):
        new_eleve = StudentDB(name=self.__name, email=self.__email)
        db.session.add(new_eleve)
        db.session.commit()

from datetime import datetime

from app.models import Teacher, Room, CourseType


class CourseSession:
    def __init__(self, teacher: Teacher, level: str, date: datetime, room : Room, course_type: CourseType):
        self.__teacher = teacher
        self.__level = level
        self.__date = date
        self.__room = room
        self.__students = []
        self.__waiting_list = []
        self.__course_type = course_type


    @property
    def teacher(self):
        return self.__teacher
    @property
    def level(self):
        return self.__level
    @property
    def date(self):
        return self.__date
    @property
    def room(self):
        return self.__room
    @property
    def students(self):
        return self.__students
    @property
    def waiting_list(self):
        return self.__waiting_list
    @property
    def course_type(self):
        return self.__course_type


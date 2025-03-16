from datetime import datetime

from app.database.tables import CourseDB
from app.models import Teacher, Room, CourseType, Student


class Course:
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

    @students.setter
    def students(self, students):
        self.__students = students
    @waiting_list.setter
    def waiting_list(self, waiting_list):
        self.__waiting_list = waiting_list

    @classmethod
    def from_db(cls, db_obj):
        """Transforme un CourseDB en Course"""
        teacher = Teacher.from_db(db_obj.teacher)
        course_type = CourseType.from_db(db_obj.course_type)
        students = [Student.from_db(student) for student in db_obj.students]
        waiting_list = [Student.from_db(student) for student in db_obj.waiting_list]

        course = cls(
            teacher=teacher,
            level=db_obj.level,
            date=db_obj.date,
            room=db_obj.room,
            course_type=course_type
        )
        course.students = students
        course.waiting_list = waiting_list
        return course

    def to_db(self):
        """Transforme un Course en CourseDB"""
        db_course = CourseDB(
            id_teacher=self.__teacher.to_db().id,
            level=self.__level,
            date=self.__date,
            room=self.__room,
            id_course_type=self.__course_type.to_db().id
        )

        db_course.students = [student.to_db() for student in self.__students]
        db_course.waiting_list = [student.to_db() for student in self.__waiting_list]

        return db_course
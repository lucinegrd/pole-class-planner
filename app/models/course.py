from app import db
from .association_tables import registration, waiting_list
from app.models import Student, Teacher, CourseType, Room, Level

class Course(db.Model):
    __tablename__ = 'course'

    # Attributs
    id = db.Column(db.Integer, primary_key=True)
    id_teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    id_level = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    id_room = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    id_course_type = db.Column(db.Integer, db.ForeignKey('course_type.id'), nullable=False)

    # Relations
    room = db.relationship(Room, backref='courses', lazy="select")
    level = db.relationship(Level, backref='courses', lazy="select")
    teacher = db.relationship(Teacher, backref="courses", lazy="select")
    course_type = db.relationship(CourseType, backref="courses", lazy="select")
    students = db.relationship(Student, secondary=registration, backref="courses", lazy="select")
    waiting_list = db.relationship(Student, secondary=waiting_list, backref="waiting_courses", lazy="select")

    @property
    def is_full(self):
        return len(self.students) >= self.course_type.places

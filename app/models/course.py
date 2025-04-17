from app import db
from app.models import Student, Teacher, CourseType, Room, Level
from .registration import Registration


class Course(db.Model):
    __tablename__ = 'course'

    # Attributs
    id = db.Column(db.Integer, primary_key=True)
    id_teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    id_level = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    id_room = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    id_course_type = db.Column(db.Integer, db.ForeignKey('course_type.id'), nullable=False)
    canceled = db.Column(db.Boolean, nullable=False, default=False)

    # Relations
    room = db.relationship(Room, backref='courses', lazy="select")
    level = db.relationship(Level, backref='courses', lazy="select")
    teacher = db.relationship(Teacher, backref="courses", lazy="select")
    course_type = db.relationship(CourseType, backref="courses", lazy="select")

    @property
    def is_full(self):
        return len(self.students_confirmed) >= self.course_type.places

    @property
    def students_confirmed(self):
        return [reg.student for reg in self.registrations if reg.state != "Annulé" and reg.state != "Sur liste d\'attente"]

    @property
    def places(self):
        return self.course_type.places - len(self.students_confirmed)

    @property
    def students(self):
        return [reg.student for reg in self.registrations]
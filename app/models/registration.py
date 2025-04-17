from datetime import datetime
from app import db


class Registration(db.Model):
    __tablename__ = "registrations"
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), primary_key=True)
    state = db.Column(db.String(50), nullable=False, default="Non validé")
    created_at = db.Column(db.DateTime, default=datetime.now)

    course = db.relationship("Course", backref=db.backref("registrations", cascade="all, delete-orphan"))
    student = db.relationship("Student", backref=db.backref("registrations", cascade="all, delete-orphan"))

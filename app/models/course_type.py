from app import db

class CourseType(db.Model):
    __tablename__ = 'course_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    places = db.Column(db.Integer, nullable=False)


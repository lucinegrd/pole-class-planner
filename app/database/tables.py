from database import db

class StudentDB(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def description(self):
        return f"{self.name}, {self.email} (id = {self.id})"

class TeacherDB(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


registration = db.Table('registrations',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True)
)

waiting_list = db.Table('waiting_list',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True)
)

class CourseTypeDB(db.Model):
    __tablename__ = 'course_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    places = db.Column(db.Integer, nullable=False)

class CourseDB(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    id_teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    level = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    room = db.Column(db.String(100), nullable=False)
    students = db.relationship("student", backref="courses", secondary="registration")
    waiting_list = db.relationship("student", secondary="waiting_list", backref="waiting_lists")
    id_course_type = db.Column(db.Integer, db.ForeignKey('course_type.id'), nullable=False)

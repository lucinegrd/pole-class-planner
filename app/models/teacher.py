from app import db
from flask_login import UserMixin

class Teacher(db.Model, UserMixin):
    __tablename__ = 'teacher'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def name(self):
        return self.first_name + " " + self.last_name

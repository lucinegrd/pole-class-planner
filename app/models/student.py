from app import db
from app.models.subscription import Subscription


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    credit_balance = db.Column(db.Integer, default=0)
    subscriptions = db.relationship(Subscription, backref="student", lazy="dynamic")


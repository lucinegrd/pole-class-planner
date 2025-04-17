from datetime import datetime

from app import db

class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    weekly_limit = db.Column(db.Integer, nullable=False)

    def is_active_on(self, date):
        return self.start_date <= date <= self.end_date

    def is_active_now(self):
        now = datetime.now()
        return self.is_active_on(now)

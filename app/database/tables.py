from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class StudentDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def description(self):
        return f"{self.name}, {self.email} (id = {self.id})"

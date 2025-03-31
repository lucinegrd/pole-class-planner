from flask import Blueprint, request, jsonify, render_template
from app import db
from app.repositories.course_repository import CourseRepository

students_bp = Blueprint("students", __name__)

@students_bp.route("/students")
def get_students():
    #students = StudentDB.query.all()
    return jsonify([student.description() for student in students])


@students_bp.route("/students/form")
def form_students():
    return render_template("pages/add_student.html")

@students_bp.route("/students/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    email = request.form["email"]

    #new_student = StudentDB(name=name, email=email)

    try:
       # db.session.add(new_student)
        db.session.commit()
        return "Élève ajouté avec succès !"
    except Exception as e:
        db.session.rollback()
        return f"Erreur: {e}", 500

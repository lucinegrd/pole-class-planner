from flask import Blueprint, request, jsonify, render_template
from app import db
from app.database.tables import StudentDB

students_bp = Blueprint("students", __name__)

@students_bp.route("/students")
def get_students():
    students = StudentDB.query.all()
    return jsonify([student.description() for student in students])

@students_bp.route("/add_student", methods=["POST"])
def add_student():
    data = request.json
    if not data or "name" not in data or "email" not in data :
        return jsonify({"error": "Données manquantes"}), 400

    try:
        new_student = StudentDB(name=data["name"], email=data["email"])
        db.session.add(new_student)
        db.session.commit()
        return jsonify({"message": f"Élève {new_student.name} ajouté avec succès !"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@students_bp.route("/form")
def form():
    return render_template("pages/add_student.html")

@students_bp.route("/add_student_form", methods=["POST"])
def add_student_form():
    name = request.form["name"]
    email = request.form["email"]
    new_student = StudentDB(name=name, email=email)

    try:
        db.session.add(new_student)
        db.session.commit()
        return "Élève ajouté avec succès !"
    except Exception as e:
        db.session.rollback()
        return f"Erreur: {e}", 500

from flask import Blueprint, request, redirect, url_for
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user

from app.models import Teacher
from app.repositories import TeacherRepository

teachers_bp = Blueprint("teachers", __name__)

@teachers_bp.route("/studio/teacher/add", methods=["POST"])
@login_required
def add_teacher():
    first = request.form.get("first_name")
    last = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not all([first, last, email, password]):
        print("Tous les champs sont requis.", "error")
        return redirect(url_for("main.studio"))

    teacher = Teacher(
        first_name=first,
        last_name=last,
        email=email,
        password_hash=generate_password_hash(password),
        role="prof"
    )
    TeacherRepository.create(teacher)
    print("Professeur ajouté avec succès !", "success")
    return redirect(url_for("main.studio"))

@teachers_bp.route("/studio/teacher/delete/<int:id>")
@login_required
def delete_teacher(id):
    teacher = TeacherRepository.get_by_id(id)
    TeacherRepository.delete(teacher)
    print("Professeur supprimé.", "success")
    return redirect(url_for("main.studio"))

@teachers_bp.route("/studio/teacher/edit/<int:id>", methods=["POST"])
@login_required
def edit_teacher(id):
    teacher = TeacherRepository.get_by_id(id)
    TeacherRepository.edit_teacher(teacher, request.form.get("first_name"), request.form.get("last_name"), request.form.get("email"))
    print("Professeur modifié avec succès.", "success")
    return redirect(url_for("main.studio"))
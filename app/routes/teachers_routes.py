from flask import Blueprint, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import login_required
from app.models import Teacher
from app.repositories import TeacherRepository
from app.services.singletons.logger_singleton import Logger

teachers_bp = Blueprint("teachers", __name__)
"""Blueprint pour la gestion des professeurs."""

@teachers_bp.route("/studio/teacher/add", methods=["POST"])
@login_required
def add_teacher():
    """Ajoute un nouveau professeur."""
    first = request.form.get("first_name")
    last = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not all([first, last, email, password]):
        flash("Tous les champs sont requis.", "danger")
        return redirect(url_for("main.studio"))

    if TeacherRepository.get_by_email(email):
        flash("Un professeur avec cet email existe déjà.", "warning")
        return redirect(url_for("main.studio"))

    teacher = Teacher(
        first_name=first,
        last_name=last,
        email=email,
        password_hash=generate_password_hash(password),
        is_admin=False
    )
    TeacherRepository.create(teacher)
    Logger().log(f"Professeur {teacher.email} ajouté avec succès !")
    return redirect(url_for("main.studio"))

@teachers_bp.route("/studio/teacher/delete/<int:id>")
@login_required
def delete_teacher(id):
    """Supprime un professeur existant."""
    teacher = TeacherRepository.get_by_id(id)
    if teacher:
        Logger().log(f"Professeur {teacher.email} supprimé.")
        TeacherRepository.delete(teacher)
    return redirect(url_for("main.studio"))

@teachers_bp.route("/studio/teacher/edit/<int:id>", methods=["POST"])
@login_required
def edit_teacher(id):
    """Modifie les informations d'un professeur existant."""
    teacher = TeacherRepository.get_by_id(id)
    if not teacher:
        flash("Professeur introuvable.", "danger")
        return redirect(url_for("main.studio"))

    TeacherRepository.edit_teacher(
        teacher,
        first_name=request.form.get("first_name"),
        last_name=request.form.get("last_name"),
        email=request.form.get("email")
    )
    Logger().log(f"Professeur {teacher.email} modifié avec succès.", "success")
    return redirect(url_for("main.studio"))

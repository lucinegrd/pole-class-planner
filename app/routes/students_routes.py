from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.repositories.student_repository import StudentRepository
from flask_login import login_required
from .auth import admin_required
from app.services.states.registration_state_base import RegistrationState
from app.models.subscription import Subscription
from app import db
from datetime import datetime, timedelta

from ..models import Student
from app.services.singletons.logger_singleton import Logger
from ..services.singletons.alert_manager_singleton import AlertManager

students_bp = Blueprint("students", __name__)
"""Blueprint pour la gestion des étudiants."""

@students_bp.route("/students")
@login_required
@admin_required
def list_students():
    """Affiche la liste des étudiants."""
    students = StudentRepository.get_all()
    return render_template("pages/students.html", students=students)

@students_bp.route("/students/form")
@login_required
@admin_required
def form_students():
    """Affiche le formulaire d'ajout d'un étudiant."""
    return render_template("pages/add_student.html")

@students_bp.route("/students/add", methods=["POST"])
@login_required
@admin_required
def add_student():
    """Ajoute un nouvel étudiant."""
    name = request.form["name"]
    email = request.form["email"]
    credit_balance = request.form.get("credit_balance", 0)

    if StudentRepository.get_by_email(email):
        flash("Un élève avec cet email existe déjà.")
        return redirect(url_for("students.form_students"))

    try:
        StudentRepository.create_student(name, email, int(credit_balance))
        Logger().log(f"Élève {email} ajouté avec succès.")
        return redirect(url_for("students.list_students"))
    except Exception as e:
        return f"Erreur: {e}", 500

@students_bp.route("/students/<int:id>")
@login_required
@admin_required
def get_student_details(id):
    """Renvoie les détails d'un étudiant sous forme de JSON."""
    student = StudentRepository.get_by_id(id)
    if not student:
        return {"error": "Introuvable"}, 404

    registrations_by_state = {}
    for r in student.registrations:
        state = r.state
        registrations_by_state.setdefault(state, []).append({
            "course_name": r.course.course_type.name,
            "date": r.course.date.strftime('%d/%m/%Y %Hh%M'),
            "teacher": f"{r.course.teacher.first_name} {r.course.teacher.last_name}"
        })

    subs = [{
        "start": s.start_date.strftime('%d/%m/%Y'),
        "end": s.end_date.strftime('%d/%m/%Y'),
        "weekly_limit": s.weekly_limit,
        "active": s.is_active_now()
    } for s in student.subscriptions]

    return {
        "name": student.name,
        "email": student.email,
        "credits": student.credit_balance,
        "registrations": registrations_by_state,
        "subscriptions": subs
    }

@students_bp.route("/students/<int:id>/add_credits", methods=["POST"])
@login_required
@admin_required
def add_credits(id):
    """Ajoute des crédits à un étudiant."""
    student = StudentRepository.get_by_id(id)
    data = request.get_json()
    student.credit_balance += int(data["amount"])
    db.session.commit()
    Logger().log(f"{data['amount']} crédits ajoutés à {student.email}")
    reevaluate_non_validated_courses(student)
    AlertManager().remove_alerts_by_type_and_student("plus_de_credit", student.id)
    return {"success": True}

@students_bp.route("/students/<int:id>/add_subscription", methods=["POST"])
@login_required
@admin_required
def add_subscription(id):
    """Ajoute un abonnement à un étudiant."""
    data = request.get_json()
    student = StudentRepository.get_by_id(id)
    start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
    weeks = int(data["months"]) * 4
    end_date = start_date + timedelta(weeks=weeks)

    sub = Subscription(
        student=student,
        start_date=start_date,
        end_date=end_date,
        weekly_limit=int(data["weekly_limit"])
    )
    db.session.add(sub)
    db.session.commit()
    Logger().log(f"Nouvel abonnement ({data['months']} mois à partir du {start_date}, {data['weekly_limit']} cours par semaine) ajoutés à {student.email}")
    reevaluate_non_validated_courses(student)
    return {"success": True}

@students_bp.route("/students/search")
@login_required
def search_students():
    """Recherche des étudiants par nom ou email."""
    q = request.args.get("q", "")
    students = Student.query.filter(
        (Student.name.ilike(f"%{q}%")) | (Student.email.ilike(f"%{q}%"))
    ).limit(5).all()

    return jsonify([
        {"id": s.id, "name": f"{s.name} {s.email}"} for s in students
    ])

def reevaluate_non_validated_courses(student):
    """Réévalue les inscriptions non validées d'un étudiant."""
    for registration in student.registrations:
        if registration.state == "Non validé":
            RegistrationState.get_state_instance(registration).validate(registration)

from datetime import datetime

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required

from app.repositories.registration_repository import RegistrationRepository
from app.routes.auth import admin_required
from app.repositories import TeacherRepository, LevelRepository, RoomRepository, CourseTypeRepository, \
    CourseRepository
from app.services.singletons.alert_manager_singleton import AlertManager
from app.services.singletons.logger_singleton import Logger
from app.services.strategies.strategy_base import StudentStrategy

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@login_required
def home():
    alerts = AlertManager().get_alerts()
    today = datetime.now()
    next_courses = CourseRepository.get_upcoming_courses(today=today, limit=5)
    return render_template("pages/home.html", alerts=alerts, next_courses=next_courses)


@main_bp.route("/studio", methods=["GET"])
@admin_required
def studio():
    teachers = TeacherRepository.get_all()
    levels = LevelRepository.get_all()
    rooms = RoomRepository.get_all()
    course_types = CourseTypeRepository.get_all()

    return render_template("pages/studio.html",
                           teachers=teachers,
                           levels=levels,
                           rooms=rooms,
                           course_types=course_types)

@main_bp.route("/logs")
@login_required
@admin_required
def show_logs():
    logger = Logger()
    return render_template("pages/logs.html", logs=logger.get_logs())


@main_bp.route("/alerts/<int:alert_id>/action", methods=["POST"])
@login_required
def handle_alert_action(alert_id):
    data = request.get_json()
    action = data.get("action")

    alert = AlertManager().get_alert_by_id(alert_id)
    if not alert:
        return jsonify({"error": "Alerte introuvable"}), 404

    student_id = alert["data"].get("student_id")
    course_id = alert["data"].get("course_id")

    try:
        if action == "valider_quand_meme":
            registration = RegistrationRepository.get_by_course_and_student(course_id, student_id)
            strategy = StudentStrategy().get_student_credit_strategy(registration.student)
            strategy.apply(registration)
            Logger().log(
                f"Validation forcée de l'inscription de {registration.student.name} au cours de {registration.course.course_type.name}")
            RegistrationRepository.update_state(registration, "Validé")

        elif action == "annuler_reservation":
            registration = RegistrationRepository.get_by_course_and_student(course_id, student_id)
            RegistrationRepository.update_state(registration, "Annulé")

        elif action == "annuler_cours":
            course = CourseRepository.get_by_id(course_id)
            course.canceled = True
            for reg in course.registrations:
                RegistrationRepository.update_state(reg, "Annulé")

        elif action == "ignorer":
            pass  # juste suppression de l'alerte

        else:
            return jsonify({"error": f"Action inconnue : {action}"}), 400

        AlertManager().remove_alert(alert_id)
        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

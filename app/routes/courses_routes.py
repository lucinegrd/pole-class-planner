
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required
from app.repositories import CourseRepository, TeacherRepository, RoomRepository, LevelRepository, CourseTypeRepository, \
    StudentRepository
from app.repositories.registration_repository import RegistrationRepository
from app.services import CourseManager
from app.services.singletons.logger_singleton import Logger
from app.services.states.registration_state_base import RegistrationState

courses_bp = Blueprint("courses", __name__)

@courses_bp.route("/courses", methods=["GET"])
@login_required
def get_courses():

    all_courses = CourseRepository.get_all()
    events = [
        {
            "id": course.id,
            "title": course.course_type.name,
            "start": course.date.isoformat(),
            "extendedProps": {
                "teacher": course.teacher.first_name,
                "level": course.level.name,
                "places": course.places,
                "duration": course.course_type.duration,
                "color":course.course_type.color,
                "colorLevel":course.level.color,
            }
        }
        for course in all_courses
    ]
    return render_template('pages/calendar.html', events=events)


@courses_bp.route("/courses/form", methods=["POST", "GET"])
@login_required
def add_courses():

    if request.method == "GET":
        teachers = TeacherRepository.get_all()
        rooms = RoomRepository.get_all()
        levels = LevelRepository.get_all()
        courses_types = CourseTypeRepository.get_all()
        return render_template("pages/add_course.html", teachers=teachers, rooms=rooms, levels=levels, courses_types=courses_types)

    form = request.form

    required_fields = ["teacher", "level", "room", "datetime", "course_type"]
    if not all(form.get(f) for f in required_fields):
        print("Tous les champs obligatoires doivent être remplis.", "error")
        return render_template(
            "pages/add_course.html",
            teachers=TeacherRepository.get_all(),
            courses_types=CourseTypeRepository.get_all(),
            levels=LevelRepository.get_all(),
            rooms=RoomRepository.get_all(),
            form_data=form
        )
    if form.get("course_type") == "autre":
        custom_fields = ["custom_name", "custom_description", "custom_duration", "custom_credit", "custom_places", "custom_color"]
        if not all(form.get(f) for f in custom_fields):
            print("Tous les champs du cours personnalisé doivent être remplis.", "error")
            return render_template(
                "pages/add_course.html",
                teachers=TeacherRepository.get_all(),
                courses_types=CourseTypeRepository.get_all(),
                levels=LevelRepository.get_all(),
                rooms=RoomRepository.get_all(),
                form_data=form
            )

    try:
        CourseManager.create_from_form(form)
        Logger().log("Cours ajouté avec succès !")
    except Exception as e:
        Logger.log(f"Erreur lors de la création du cours : {str(e)}")

    return redirect(url_for("courses.add_courses"))


@courses_bp.route("/courses/<int:id>")
@login_required
def get_course_details(id):
    course = CourseRepository.get_by_id(id)
    if not course:
        return {"error": "Cours introuvable"}, 404

    ct = course.course_type

    return {
        "id": course.id,
        "type": ct.name,
        "description": ct.description,
        "duration": ct.duration,
        "credit": ct.credit,
        "places": ct.places,
        "color": ct.color,
        "level": course.level.name,
        "date": course.date.strftime('%d/%m/%Y à %Hh%M'),
        "teacher": f"{course.teacher.first_name} {course.teacher.last_name}",
        "room": course.room.name,
        "students": [
            {
                "name": reg.student.name,
                "state": reg.state,
                "student_id": reg.student.id
            }
            for reg in course.registrations
        ]
    }

@courses_bp.route("/courses/<int:id>/detail")
@login_required
def course_detail(id):
    course = CourseRepository.get_by_id(id)
    return render_template("pages/course_detail.html", course=course)


@courses_bp.route("/courses/<int:course_id>/<int:student_id>/confirm", methods=["POST"])
@login_required
def confirm_presence(course_id, student_id):
    registration = CourseManager.confirm_presence(course_id, student_id)
    return jsonify(success=True, new_state=registration.state)

@courses_bp.route("/courses/<int:course_id>/<int:student_id>/add", methods=['POST'])
@login_required
def add_student_to_course(course_id, student_id):
    course = CourseRepository.get_by_id(course_id)
    student = StudentRepository.get_by_id(student_id)

    try:
        CourseManager.add_student(course, student)
        return jsonify(success=True)
    except ValueError as e:
        return jsonify(success=False, message=str(e)), 400

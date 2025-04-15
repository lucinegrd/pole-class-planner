
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.repositories import CourseRepository, TeacherRepository, RoomRepository, LevelRepository, CourseTypeRepository
from app.services import CourseManager

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
        print("Cours ajouté avec succès !", "success")
    except Exception as e:
        print(f"Erreur lors de la création du cours : {str(e)}")

    return redirect(url_for("courses.add_courses"))

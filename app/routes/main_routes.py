from flask import Blueprint, request, jsonify, render_template

from app.repositories import TeacherRepository, LevelRepository, RoomRepository, CourseTypeRepository

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("partials/base.html")

@main_bp.route("/studio", methods=["GET"])
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


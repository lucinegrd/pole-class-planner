from flask import Blueprint, request, redirect, url_for
from flask_login import login_required

from app import db
from app.models import CourseType
from app.repositories import CourseTypeRepository
from app.services.singletons.logger_singleton import Logger

course_type_bp = Blueprint("course_type", __name__)


@course_type_bp.route("/studio/course_type/add", methods=["POST"])
@login_required
def add_course_type():
    name = request.form.get("name")
    description = request.form.get("description")
    duration = request.form.get("duration")
    credit = request.form.get("credit")
    places = request.form.get("places")

    if not all([name, description, duration, credit, places]):
        print("Tous les champs sont requis.", "error")
        return redirect(url_for("main.studio"))

    course_type = CourseType(
        name=name,
        description=description,
        duration=int(duration),
        credit=int(credit),
        places=int(places)
    )
    CourseTypeRepository.create(course_type)
    Logger().log("Type de cours ajouté.")
    return redirect(url_for("main.studio"))

@course_type_bp.route("/studio/course_type/delete/<int:id>")
@login_required
def delete_course_type(id):
    course_type = CourseTypeRepository.get_by_id(id)
    CourseTypeRepository.delete(course_type)
    Logger().log("Type de cours supprimé.")
    return redirect(url_for("main.studio"))

@course_type_bp.route("/studio/course_type/edit/<int:id>", methods=["POST"])
@login_required
def edit_course_type(id):
    ct = CourseTypeRepository.get_by_id(id)
    ct.name = request.form.get("name")
    ct.description = request.form.get("description")
    ct.duration = int(request.form.get("duration"))
    ct.credit = int(request.form.get("credit"))
    ct.places = int(request.form.get("places"))
    ct.color = request.form.get("color")
    db.session.commit()
    Logger().log("Type de cours modifié.")
    return redirect(url_for("main.studio"))
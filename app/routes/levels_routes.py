from flask import Blueprint, request, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.models import Level
from app.repositories import LevelRepository

level_bp = Blueprint("level", __name__)

@level_bp.route("/studio/level/add", methods=["POST"])
@login_required
def add_level():
    name = request.form.get("name")
    if not name:
        print("Nom requis.", "error")
        return redirect(url_for("main.studio"))
    color = request.form.get("color")
    if not color:
        print("Color requis.", "error")
        return redirect(url_for("main.studio"))
    level = Level(name=name, color=color)
    LevelRepository.create(level)
    print("Niveau ajouté.", "success")
    return redirect(url_for("main.studio"))

@level_bp.route("/studio/level/delete/<int:id>")
@login_required
def delete_level(id):
    level = LevelRepository.get_by_id(id)
    LevelRepository.delete(level)
    print("Niveau supprimé.", "success")
    return redirect(url_for("main.studio"))

@level_bp.route("/studio/level/edit/<int:id>", methods=["POST"])
@login_required
def edit_level(id):
    level = Level.query.get_or_404(id)
    level.name = request.form.get("name")
    db.session.commit()
    print("Niveau modifié.", "success")
    return redirect(url_for("main.studio"))

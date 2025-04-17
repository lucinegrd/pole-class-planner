from flask import Blueprint, request, redirect, url_for
from flask_login import login_required

from app import db
from app.models import Level
from app.repositories import LevelRepository
from app.services.singletons.logger_singleton import Logger

level_bp = Blueprint("level", __name__)
"""Blueprint pour la gestion des niveaux."""

@level_bp.route("/studio/level/add", methods=["POST"])
@login_required
def add_level():
    """Ajoute un nouveau niveau."""
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
    Logger().log("Niveau ajouté.")
    return redirect(url_for("main.studio"))

@level_bp.route("/studio/level/delete/<int:id>")
@login_required
def delete_level(id):
    """Supprime un niveau existant."""
    level = LevelRepository.get_by_id(id)
    LevelRepository.delete(level)
    Logger().log("Niveau supprimé.")
    return redirect(url_for("main.studio"))

@level_bp.route("/studio/level/edit/<int:id>", methods=["POST"])
@login_required
def edit_level(id):
    """Modifie un niveau existant."""
    level = Level.query.get_or_404(id)
    level.name = request.form.get("name")
    db.session.commit()
    Logger().log("Niveau modifié.")
    return redirect(url_for("main.studio"))

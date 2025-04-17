from flask import Blueprint, request, redirect, url_for
from flask_login import login_required

from app import db
from app.models import Room
from app.repositories import RoomRepository
from app.services.singletons.logger_singleton import Logger

room_bp = Blueprint("room", __name__)
"""Blueprint pour la gestion des salles."""

@room_bp.route("/studio/room/add", methods=["POST"])
@login_required
def add_room():
    """Ajoute une nouvelle salle."""
    name = request.form.get("name")
    if not name:
        print("Nom requis.", "error")
        return redirect(url_for("main.studio"))
    room = Room(name=name)
    RoomRepository.create(room)
    Logger().log("Salle ajoutée.")
    return redirect(url_for("main.studio"))

@room_bp.route("/studio/room/delete/<int:id>")
@login_required
def delete_room(id):
    """Supprime une salle existante."""
    room = RoomRepository.get_by_id(id)
    RoomRepository.delete(room)
    Logger().log("Salle supprimée.")
    return redirect(url_for("main.studio"))

@room_bp.route("/studio/room/edit/<int:id>", methods=["POST"])
@login_required
def edit_room(id):
    """Modifie les informations d'une salle existante."""
    room = RoomRepository.get_by_id(id)
    room.name = request.form.get("name")
    db.session.commit()
    Logger().log("Salle modifiée.")
    return redirect(url_for("main.studio"))

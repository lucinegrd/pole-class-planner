from flask import Blueprint, request, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.models import Room
from app.repositories import RoomRepository

room_bp = Blueprint("room", __name__)

@room_bp.route("/studio/room/add", methods=["POST"])
@login_required
def add_room():
    name = request.form.get("name")
    if not name:
        print("Nom requis.", "error")
        return redirect(url_for("main.studio"))
    room = Room(name=name)
    RoomRepository.create(room)
    print("Salle ajoutée.", "success")
    return redirect(url_for("main.studio"))

@room_bp.route("/studio/room/delete/<int:id>")
@login_required
def delete_room(id):
    room = RoomRepository.get_by_id(id)
    RoomRepository.delete(room)
    print("Salle supprimée.", "success")
    return redirect(url_for("main.studio"))

@room_bp.route("/studio/room/edit/<int:id>", methods=["POST"])
@login_required
def edit_room(id):
    room = RoomRepository.get_by_id(id)
    room.name = request.form.get("name")
    db.session.commit()
    print("Salle modifiée.", "success")
    return redirect(url_for("main.studio"))
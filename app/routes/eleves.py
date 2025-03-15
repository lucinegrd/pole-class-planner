from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models.eleve import Eleve
from app.services.eleve_factory import EleveFactory

eleves_bp = Blueprint("eleves", __name__)

@eleves_bp.route("/eleves")
def get_eleves():
    eleves = Eleve.query.all()
    return jsonify([eleve.description() for eleve in eleves])

@eleves_bp.route("/add_eleve", methods=["POST"])
def add_eleve():
    data = request.json
    if not data or "nom" not in data or "email" not in data or "type" not in data:
        return jsonify({"error": "Données manquantes"}), 400

    try:
        new_eleve = EleveFactory.create_eleve(data["type"], data["nom"], data["email"], data.get("niveau"))
        db.session.add(new_eleve)
        db.session.commit()
        return jsonify({"message": f"Élève {new_eleve.nom} ajouté avec succès !"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@eleves_bp.route("/form")
def form():
    return render_template("pages/add_eleve.html")

@eleves_bp.route("/add_eleve_form", methods=["POST"])
def add_eleve_form():
    nom = request.form["nom"]
    email = request.form["email"]
    new_eleve = Eleve(nom, email)

    try:
        db.session.add(new_eleve)
        db.session.commit()
        return "Élève ajouté avec succès !"
    except Exception as e:
        db.session.rollback()
        return f"Erreur: {e}", 500

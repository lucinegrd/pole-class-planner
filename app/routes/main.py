from flask import Blueprint, request, jsonify, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("partials/base.html")

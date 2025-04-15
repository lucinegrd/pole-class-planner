from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app.repositories import TeacherRepository
from functools import wraps
from flask import abort
from flask_login import current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        teacher = TeacherRepository.get_by_email(email)

        if teacher and check_password_hash(teacher.password_hash, password):
            login_user(teacher)
            flash("Connexion réussie.")
            return redirect(url_for("main.home"))
        else:
            flash("Email ou mot de passe invalide.")

    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


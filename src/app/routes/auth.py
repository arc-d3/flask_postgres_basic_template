from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegisterForm
from app.services.auth_service import register_user, authenticate_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if form.validate_on_submit():
        user_record = authenticate_user(
            email = form.email.data,
            password = form.password.data
        )

        if user_record:
            login_user(user_record)
            return redirect(url_for("main.dashboard"))
        
        flash("Invalid email or password")
    return render_template("login.html", form=form)
    
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        is_success = register_user(
            name = form.name.data,
            email = form.email.data,
            password = form.password.data
        )
        if is_success:
            flash("Registration Success")
            return redirect(url_for("auth.login"))
        
        flash("Email Taken")
    return render_template("register.html", form=form)
    
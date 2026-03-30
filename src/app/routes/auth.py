from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import LoginForm, RegisterForm

from app.models.user import User
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if form.validate_on_submit():
        # start authenticate
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar_one_or_none()
        if user and user.check_password(form.password.data):
            login_user(user)
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
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar_one_or_none()
        if user:
            flash("Email Taken")
            return render_template("register.html", form=form)
        
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Registration Success")
        return redirect(url_for("auth.login"))
    
    return render_template("register.html", form=form)
    
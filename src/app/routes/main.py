from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import ApiKeyRegisterForm
from app.services.api_key_service import create_api_key, get_all_api_keys

from app.models.user import User
main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@main_bp.route("/home")
def home():
    return render_template("home.html")

@main_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard.html")

@main_bp.route("/dashboard/keys", methods=["GET","POST"])
@login_required
def api_keys():
    
    form = ApiKeyRegisterForm()

    if form.validate_on_submit():

        api_key = create_api_key(
            user_id=current_user.id,
            name=form.name.data
        )

        if api_key:
            flash("Create API Key Success")
            return redirect(url_for("main.api_keys"))
        
        flash("Error Creating API Key")
    
    keys = get_all_api_keys(current_user.id)
    return render_template("api_key.html", form=form, keys=keys)
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app import db
from app.forms import LoginForm

from app.models.user import User
main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@main_bp.route("/home")
def home():
    return "This is Home"

@main_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return "This is dashboard"
# ============================================================
# AUTHENTICATION BLUEPRINT
# - Register new users (hashed passwords)
# - Login/logout with Flask-Login sessions
# ============================================================

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from db import db
from models import User


# ================= BLUEPRINT SETUP =================
auth_bp = Blueprint("auth", __name__)


# ================= REGISTRATION =================
@auth_bp.get("/register")
def register_form():
    return render_template("register.html")


# ============================================================
# bookly — Flask application entry point
# - Creates and configures the Flask app
# - Initialises extensions (SQLAlchemy + Flask-Login)
# - Registers blueprints (auth, books, cart, orders, admin)
# - Provides a couple of top-level routes (home/contact) + 403 page
# ============================================================

import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager

from cli import register_cli
from config import Config
from db import db
from models import User


def create_app() -> Flask:
    # ================= ENVIRONMENT + APP CONFIG =================
    load_dotenv()  # loads .env in dev; production uses real environment variables

    app = Flask(__name__)
    app.config.from_object(Config)

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError(
            "DATABASE_URL is missing. Create a .env file (see .env.example)."
        )

    # ================= DATABASE (SQLALCHEMY) =================
    db.init_app(app)

    # ================= AUTH SESSION (FLASK-LOGIN) =================
    login_manager = LoginManager()
    login_manager.login_view = "auth.login_form"  # where @login_required sends guests
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        # Flask-Login calls this with the user id stored in the session cookie.
        try:
            uid = int(user_id)
        except ValueError:
            return None
        return User.query.get(uid)


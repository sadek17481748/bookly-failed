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
    # ================= DATABASE (SQLALCHEMY) =================
    db.init_app(app)

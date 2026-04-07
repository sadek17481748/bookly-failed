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

    # ================= BLUEPRINTS (FEATURE ROUTES) =================
    # Routes live in auth.py, books.py, cart.py, orders.py, admin.py.
    from auth import auth_bp
    from admin import admin_bp
    from books import books_bp
    from cart import cart_bp
    from orders import orders_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)

    # ================= SIMPLE PAGES (NON-BLUEPRINT) =================
    @app.get("/")
    def home():
        return render_template("home.html")

    @app.get("/contact")
    def contact():
        return render_template("contact.html")

    # ================= ERROR PAGES =================
    @app.errorhandler(403)
    def forbidden(_err):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def not_found(_err):
        return render_template("404.html"), 404

    # ================= FLASK CLI COMMANDS =================
    # init-db, reset-db, make-admin
    register_cli(app)
    return app


# ============================================================
# APP INSTANCE
# - Used by `flask --app app` and by gunicorn (`app:app`)
# ============================================================
app = create_app()


if __name__ == "__main__":
    # ================= LOCAL DEVELOPMENT RUNNER =================
    port = int(os.environ.get("PORT", "5000"))  # Heroku sets PORT
    app.run(host="0.0.0.0", port=port, debug=True)

# ============================================================
# FLASK CONFIGURATION
# - Reads secrets and database URL from environment variables
# - Avoids hard-coding real credentials in source control
# ============================================================

import os


class Config:
    # ================= SESSION / SECURITY =================
    # Session signing / CSRF (use a long random string in production).
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    # ================= DATABASE URL =================
    # Example: postgresql+psycopg2://user:pass@host:5432/dbname
    _db_url = os.environ.get("DATABASE_URL")
    # Heroku provides DATABASE_URL as postgres://..., but SQLAlchemy expects postgresql://...
    if _db_url and _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _db_url
    # ================= SQLALCHEMY SETTINGS =================
    SQLALCHEMY_TRACK_MODIFICATIONS = False

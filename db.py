# ============================================================
# DATABASE EXTENSION (SQLAlchemy)
# - Shared SQLAlchemy() instance
# - Imported by models + blueprints so the app uses one db session/metadata
# ============================================================

from flask_sqlalchemy import SQLAlchemy


# ================= SQLALCHEMY INSTANCE =================
db = SQLAlchemy()

# ============================================================
# DATABASE MODELS (SQLAlchemy)
# - Table names match schema.sql
# - Money values are stored as integer cents (no floating point)
# - Relationships connect users ↔ reviews/cart/orders ↔ books
# ============================================================

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from db import db


# ================= USERS (LOGIN + CART + ORDERS) =================
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")
    cart_items = db.relationship(
        "CartItem", back_populates="user", cascade="all, delete-orphan"
    )
    orders = db.relationship("Order", back_populates="user")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


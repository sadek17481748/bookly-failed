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


# ================= BOOK CATALOG =================
class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    author = db.Column(db.String(255), nullable=False, index=True)
    category = db.Column(db.String(255), nullable=False, default="Uncategorized", index=True)
    price_cents = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    cover_url = db.Column(db.String(1024), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    reviews = db.relationship("Review", back_populates="book", cascade="all, delete-orphan")

    def price_dollars(self) -> str:
        return f"{self.price_cents / 100:.2f}"


# ================= REVIEWS (USER ↔ BOOK) =================
class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1–5
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="reviews")
    book = db.relationship("Book", back_populates="reviews")


# ================= SHOPPING CART =================
# One row per (user, book). Quantity is stored on the row.
class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="cart_items")
    book = db.relationship("Book")

    __table_args__ = (db.UniqueConstraint("user_id", "book_id", name="uq_cart_user_book"),)


# ================= ORDERS =================
# Header row + line items (unit price snapshot stored at checkout time).
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    total_cents = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


# ================= ORDER ITEMS =================
class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price_cents = db.Column(db.Integer, nullable=False)  # copy of book price at checkout time

    order = db.relationship("Order", back_populates="items")
    book = db.relationship("Book")

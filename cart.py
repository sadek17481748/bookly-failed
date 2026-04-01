# ============================================================
# CART BLUEPRINT
# - Database-backed cart (cart_items table)
# - Add, update quantity, remove items
# - Requires authentication (per-user cart)
# ============================================================

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from db import db
from models import Book, CartItem


# ================= BLUEPRINT SETUP =================
cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


def _cart_totals(items):
    # ================= SUBTOTAL HELPER =================
    # Sums line totals in cents (expects each item.book loaded).
    subtotal_cents = 0
    for item in items:
        subtotal_cents += item.book.price_cents * item.quantity
    return subtotal_cents


# ================= VIEW CART (LOGIN REQUIRED) =================
@cart_bp.get("")
@login_required
def view_cart():
    # -------- Load cart items for the current user --------
    items = (
        CartItem.query.filter_by(user_id=current_user.id)
        .join(Book, Book.id == CartItem.book_id)
        .all()
    )
    # -------- Calculate totals --------
    subtotal_cents = _cart_totals(items)
    return render_template("cart.html", items=items, subtotal_cents=subtotal_cents)


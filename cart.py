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



# ============================================================
# ORDERS + CHECKOUT BLUEPRINT
# - Order history for the logged-in user
# - Checkout flow: create Order + OrderItem rows from cart_items
# - Clears cart after successful checkout
# ============================================================

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from db import db
from models import CartItem, Order, OrderItem


# ================= BLUEPRINT SETUP =================
orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


# ================= ORDER HISTORY (LOGIN REQUIRED) =================
@orders_bp.get("")
@login_required
def list_orders():
    # -------- Load orders for the current user --------
    orders = (
        Order.query.filter_by(user_id=current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return render_template("orders.html", orders=orders)


# ================= CHECKOUT FORM (LOGIN REQUIRED) =================
# GET shows shipping form + current cart summary.
@orders_bp.get("/checkout")
@login_required
def checkout_form():
    # -------- Load cart items for the current user --------
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    # -------- Calculate subtotal for display --------
    subtotal_cents = sum(item.book.price_cents * item.quantity for item in items)
    return render_template("checkout.html", items=items, subtotal_cents=subtotal_cents)


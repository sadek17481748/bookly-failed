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


# ================= CHECKOUT SUBMIT (LOGIN REQUIRED) =================
# POST creates Order + OrderItem rows, then clears cart.
@orders_bp.post("/checkout")
@login_required
def checkout_submit():
    # -------- Load cart rows --------
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash("Your cart is empty.", "error")
        return redirect(url_for("cart.view_cart"))

    # -------- Read shipping fields --------
    full_name = (request.form.get("full_name") or "").strip()
    address = (request.form.get("address") or "").strip()

    # -------- Validate checkout form --------
    if not full_name or not address:
        flash("Name and address are required for checkout.", "error")
        return redirect(url_for("orders.checkout_form"))

    # -------- Create order header row --------
    total_cents = sum(item.book.price_cents * item.quantity for item in items)
    order = Order(user_id=current_user.id, total_cents=total_cents)
    db.session.add(order)
    db.session.flush()  # get order.id before inserting order_items

    # -------- Create order item rows (price snapshot) --------
    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            book_id=item.book_id,
            quantity=item.quantity,
            unit_price_cents=item.book.price_cents,
        )
        db.session.add(order_item)

    # -------- Clear cart rows after creating order --------
    for item in items:
        db.session.delete(item)

    # -------- Commit and redirect --------
    db.session.commit()
    flash("Purchase complete! Your order has been created.", "success")
    return redirect(url_for("orders.list_orders"))

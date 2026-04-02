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


# ================= ADD TO CART (LOGIN REQUIRED) =================
# Merges quantity if the same book is already in the cart (unique user+book in DB).
@cart_bp.post("/add/<int:book_id>")
@login_required
def add_to_cart(book_id: int):
    # -------- Load book and read quantity input --------
    book = Book.query.get_or_404(book_id)
    qty_raw = request.form.get("quantity") or "1"

    try:
        qty = int(qty_raw)
    except ValueError:
        qty = 1

    # -------- Guard against invalid quantities --------
    if qty < 1:
        qty = 1

    # -------- Insert new row or merge quantity --------
    item = CartItem.query.filter_by(user_id=current_user.id, book_id=book.id).first()
    if item is None:
        item = CartItem(user_id=current_user.id, book_id=book.id, quantity=qty)
        db.session.add(item)
    else:
        item.quantity += qty

    # -------- Save and redirect --------
    db.session.commit()
    flash(f"Added to cart: {book.title}", "success")
    return redirect(url_for("cart.view_cart"))


# ================= UPDATE QUANTITY (LOGIN REQUIRED) =================
# Quantity < 1 removes the row.
@cart_bp.post("/update/<int:item_id>")
@login_required
def update_quantity(item_id: int):
    # -------- Fetch the cart row scoped to the current user --------
    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    qty_raw = request.form.get("quantity") or "1"

    try:
        qty = int(qty_raw)
    except ValueError:
        qty = 1

    # -------- Apply update or delete --------
    if qty < 1:
        db.session.delete(item)
    else:
        item.quantity = qty

    # -------- Save and redirect --------
    db.session.commit()
    flash("Cart updated.", "success")
    return redirect(url_for("cart.view_cart"))


# ================= REMOVE ITEM (LOGIN REQUIRED) =================
@cart_bp.post("/remove/<int:item_id>")
@login_required
def remove_item(item_id: int):
    # -------- Fetch and delete the cart row --------
    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash("Removed from cart.", "success")
    return redirect(url_for("cart.view_cart"))

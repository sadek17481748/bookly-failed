# ============================================================
# ADMIN BLUEPRINT (ANALYTICS)
# - Admin-only dashboard (requires User.is_admin)
# - Uses SQL aggregates (COUNT/SUM/GROUP BY) for KPI reporting
# ============================================================

from functools import wraps

from pathlib import Path

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc, func

from db import db
from models import Book, Order, OrderItem, Review, User


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view_func):
    # ================= ADMIN-ONLY DECORATOR =================
    # Wraps a view so only logged-in users with is_admin=True can open it.

    @wraps(view_func)
    @login_required
    def wrapper(*args, **kwargs):
        # Reject non-admin users with a 403 page.
        if not getattr(current_user, "is_admin", False):
            abort(403)
        return view_func(*args, **kwargs)

    return wrapper


# ================= ANALYTICS DASHBOARD =================
# KPIs, top sellers, recent orders, books per category.
@admin_bp.get("/analytics")
@admin_required
def analytics_dashboard():
    # -------- KPI counts --------
    total_users = db.session.query(func.count(User.id)).scalar() or 0
    total_reviews = db.session.query(func.count(Review.id)).scalar() or 0
    total_orders = db.session.query(func.count(Order.id)).scalar() or 0
    revenue_cents = db.session.query(func.coalesce(func.sum(Order.total_cents), 0)).scalar() or 0
    avg_order_cents = 0
    if total_orders > 0:
        avg_order_cents = int(revenue_cents / total_orders)

    # -------- Recent orders --------
    recent_orders = (
        Order.query.order_by(Order.created_at.desc())
        .limit(10)
        .all()
    )

    # -------- Top-selling books --------
    top_books = (
        db.session.query(
            Book.id,
            Book.title,
            Book.author,
            Book.category,
            func.coalesce(func.sum(OrderItem.quantity), 0).label("qty"),
            func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price_cents), 0).label(
                "sales_cents"
            ),
        )
        .join(OrderItem, OrderItem.book_id == Book.id)
        .group_by(Book.id)
        .order_by(desc("qty"))
        .limit(10)
        .all()
    )

    # -------- Catalogue breakdown --------
    books_by_category = (
        db.session.query(Book.category, func.count(Book.id).label("count"))
        .group_by(Book.category)
        .order_by(desc("count"))
        .all()
    )

    # -------- Render dashboard template --------
    return render_template(
        "admin_analytics.html",
        total_users=total_users,
        total_reviews=total_reviews,
        total_orders=total_orders,
        revenue_cents=revenue_cents,
        avg_order_cents=avg_order_cents,
        recent_orders=recent_orders,
        top_books=top_books,
        books_by_category=books_by_category,
    )


# ================= ADMIN: ADD BOOK =================
@admin_bp.get("/books/new")
@admin_required
def new_book_form():
    # -------- Provide cover choices from static assets --------
    covers_dir = Path(__file__).resolve().parent / "static" / "img" / "covers"
    cover_files: list[str] = []
    if covers_dir.exists():
        for p in sorted(covers_dir.iterdir()):
            if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".svg"}:
                cover_files.append(p.name)

    # -------- Suggest existing categories (still allow free text) --------
    existing_categories = [
        row[0]
        for row in db.session.query(Book.category)
        .distinct()
        .order_by(Book.category.asc())
        .all()
        if row[0]
    ]

    return render_template(
        "admin_add_book.html",
        cover_files=cover_files,
        existing_categories=existing_categories,
    )


@admin_bp.post("/books/new")
@admin_required
def new_book_submit():
    title = (request.form.get("title") or "").strip()
    author = (request.form.get("author") or "").strip()
    category = (request.form.get("category") or "").strip() or "Uncategorized"
    description = (request.form.get("description") or "").strip()
    price_raw = (request.form.get("price") or "").strip()
    cover_filename = (request.form.get("cover_filename") or "").strip()

    # -------- Validate required fields --------
    errors: list[str] = []
    if not title:
        errors.append("Title is required.")
    if not author:
        errors.append("Author is required.")
    if not price_raw:
        errors.append("Price is required.")

    # -------- Parse price into cents (e.g. 12.99 -> 1299) --------
    price_cents = 0
    if price_raw:
        try:
            price_float = float(price_raw)
            price_cents = int(round(price_float * 100))
        except ValueError:
            errors.append("Price must be a number (e.g. 12.99).")

    if price_cents <= 0:
        errors.append("Price must be greater than 0.")

    # -------- Optional cover selection --------
    cover_url = None
    if cover_filename:
        covers_dir = Path(__file__).resolve().parent / "static" / "img" / "covers"
        chosen = covers_dir / cover_filename
        if not chosen.exists():
            errors.append("Selected cover image does not exist.")
        else:
            cover_url = f"/static/img/covers/{cover_filename}"

    # -------- Duplicate prevention (title + author) --------
    if title and author:
        existing = Book.query.filter_by(title=title, author=author).first()
        if existing is not None:
            errors.append("That book already exists in the catalogue.")

    if errors:
        for msg in errors:
            flash(msg, "error")
        return redirect(url_for("admin.new_book_form"))

    book = Book(
        title=title,
        author=author,
        category=category,
        price_cents=price_cents,
        description=description,
        cover_url=cover_url,
    )
    db.session.add(book)
    db.session.commit()

    flash("Book added to catalogue.", "success")
    return redirect(url_for("books.book_detail", book_id=book.id))

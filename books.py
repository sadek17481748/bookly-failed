# ============================================================
# BOOKS + REVIEWS BLUEPRINT
# - Public catalogue pages: list + detail
# - Logged-in actions: create review
# - Owner-only actions: edit / delete review
# ============================================================

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from db import db
from models import Book, Review


# ================= BLUEPRINT SETUP =================
books_bp = Blueprint("books", __name__, url_prefix="/books")


# ================= BOOK LIST + SEARCH =================
# Optional query parameter: ?q= searches title and author (case-insensitive).
@books_bp.get("")
def list_books():
    q = (request.args.get("q") or "").strip()
    query = Book.query
    if q:
        like = f"%{q}%"
        query = query.filter((Book.title.ilike(like)) | (Book.author.ilike(like)))

    books = query.order_by(Book.created_at.desc()).all()
    return render_template("books.html", books=books, q=q)


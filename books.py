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


# ================= BOOK DETAIL + REVIEW LIST =================
@books_bp.get("/<int:book_id>")
def book_detail(book_id: int):
    book = Book.query.get_or_404(book_id)
    reviews = (
        Review.query.filter_by(book_id=book_id)
        .order_by(Review.created_at.desc())
        .all()
    )
    return render_template("book_detail.html", book=book, reviews=reviews)


# ================= CREATE REVIEW (LOGIN REQUIRED) =================
@books_bp.post("/<int:book_id>/reviews")
@login_required
def create_review(book_id: int):
    # -------- Load book + read form values --------
    book = Book.query.get_or_404(book_id)
    rating_raw = request.form.get("rating") or ""
    body = (request.form.get("body") or "").strip()

    # -------- Validate rating is an integer 1–5 --------
    try:
        rating = int(rating_raw)
    except ValueError:
        rating = 0

    if rating < 1 or rating > 5:
        flash("Rating must be between 1 and 5.", "error")
        return redirect(url_for("books.book_detail", book_id=book.id))

    # -------- Validate review body is not empty --------
    if not body:
        flash("Review text is required.", "error")
        return redirect(url_for("books.book_detail", book_id=book.id))

    # -------- Insert review row linked to current user --------
    review = Review(user_id=current_user.id, book_id=book.id, rating=rating, body=body)
    db.session.add(review)
    db.session.commit()

    flash("Review posted!", "success")
    return redirect(url_for("books.book_detail", book_id=book.id))


# ================= DELETE REVIEW (OWNER ONLY) =================
@books_bp.post("/<int:book_id>/reviews/<int:review_id>/delete")
@login_required
def delete_review(book_id: int, review_id: int):
    # -------- Fetch review scoped to the book --------
    review = Review.query.filter_by(id=review_id, book_id=book_id).first_or_404()

    # -------- Ownership check (server-side) --------
    if review.user_id != current_user.id:
        flash("You can only delete your own reviews.", "error")
        return redirect(url_for("books.book_detail", book_id=book_id))

    # -------- Delete row and save --------
    db.session.delete(review)
    db.session.commit()

    flash("Review deleted.", "success")
    return redirect(url_for("books.book_detail", book_id=book_id))


# ================= EDIT REVIEW (OWNER ONLY) =================
# Form page + POST handler.
@books_bp.get("/<int:book_id>/reviews/<int:review_id>/edit")
@login_required
def edit_review_form(book_id: int, review_id: int):
    review = Review.query.filter_by(id=review_id, book_id=book_id).first_or_404()

    # -------- Ownership check (server-side) --------
    if review.user_id != current_user.id:
        flash("You can only edit your own reviews.", "error")
        return redirect(url_for("books.book_detail", book_id=book_id))

    book = Book.query.get_or_404(book_id)
    return render_template("edit_review.html", book=book, review=review)


@books_bp.post("/<int:book_id>/reviews/<int:review_id>/edit")
@login_required
def edit_review_submit(book_id: int, review_id: int):
    review = Review.query.filter_by(id=review_id, book_id=book_id).first_or_404()

    # -------- Ownership check (server-side) --------
    if review.user_id != current_user.id:
        flash("You can only edit your own reviews.", "error")
        return redirect(url_for("books.book_detail", book_id=book_id))

    # -------- Read + validate form values --------
    rating_raw = request.form.get("rating") or ""
    body = (request.form.get("body") or "").strip()

    try:
        rating = int(rating_raw)
    except ValueError:
        rating = 0

    if rating < 1 or rating > 5:
        flash("Rating must be between 1 and 5.", "error")
        return redirect(
            url_for("books.edit_review_form", book_id=book_id, review_id=review_id)
        )

    if not body:
        flash("Review text is required.", "error")
        return redirect(
            url_for("books.edit_review_form", book_id=book_id, review_id=review_id)
        )

    # -------- Apply updates and save --------
    review.rating = rating
    review.body = body
    db.session.commit()

    flash("Review updated.", "success")
    return redirect(url_for("books.book_detail", book_id=book_id))

# Legacy Code Snapshots (Before Improvements)

This file preserves **small excerpts** of earlier implementations that were later improved during development. It exists for coursework review so an assessor can see examples of “old code” and understand what was changed and why.

> **Notes:**
> - These snippets are **representative excerpts**, not full files.
> - The “after” versions are present in the current codebase; the “before” versions are shown here for comparison.

---

## 1) Book Cover URLs (SVG-only → prefer raster covers + SVG fallback)

### Before (SVG-only)

```python
def cover_static_url(title: str) -> str:
    """URL path served by Flask static (see static/img/covers/*.svg)."""
    return f"/static/img/covers/{slug_for_title(title)}.svg"
```

### After (prefer `.png`/`.jpg`/`.webp`, fallback to SVG)

```python
def cover_static_url(title: str) -> str:
    slug = slug_for_title(title)
    for ext in (".png", ".jpg", ".jpeg", ".webp", ".svg"):
        if (covers_dir / f"{slug}{ext}").exists():
            return f"/static/img/covers/{slug}{ext}"
    return f"/static/img/covers/{slug}.svg"
```

---

## 2) Seeding Behavior (`init-db` only seeded empty DB → backfill/upgrade existing rows)

### Before (seed only if the catalogue is empty)

```python
def _seed_books_if_empty() -> None:
    if Book.query.count() != 0:
        return
    db.session.add_all(seed_books)
    db.session.commit()
```

### After (insert missing titles and backfill/upgrade `cover_url`)

```python
def _seed_books() -> None:
    for seeded in seed_books:
        existing = Book.query.filter_by(title=seeded.title).first()
        if existing is None:
            db.session.add(seeded)
            continue

        if (not existing.cover_url) or (
            existing.cover_url.endswith(".svg") and existing.cover_url != seeded.cover_url
        ):
            existing.cover_url = seeded.cover_url

    db.session.commit()
```

---

## 3) Manual Testing Evidence (paths were plain text → clickable links)

### Before (plain text paths)

```markdown
| 1 | Public | Open `/` | Home loads |  |  | `docs/images/manual-testing/01-home.png` |
```

### After (clickable links)

```markdown
| 1 | Public | Open `/` | Home loads |  |  | [01-home](docs/images/manual-testing/01-home.png) |
```

---

## 4) Seed Script (`seed.py`)

```python
from yourapp import app, db
from models import Book, User

with app.app_context():
    db.drop_all()
    db.create_all()
    # Add sample data
    book = Book(title="Sample Book", author="Author")
    db.session.add(book)
    db.session.commit()
```

---

## 5) Book Management (Add New Book - Admin Route)

```python
@app.route("/admin/books/new", methods=["GET", "POST"])
@login_required
@admin_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            category=form.category.data,
            price=form.price.data,
            description=form.description.data,
            cover_url=form.cover_url.data,
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("list_books"))
    return render_template("admin/new_book.html", form=form)
```

---

## 6) Cart Management

```python
@app.route("/cart/add/<int:book_id>", methods=["POST"])
@login_required
def add_to_cart(book_id):
    quantity = int(request.form.get("quantity", 1))
    cart = session.get("cart", {})
    cart[book_id] = cart.get(book_id, 0) + quantity
    session["cart"] = cart
    return redirect(url_for("cart_view"))


@app.route("/cart")
def cart_view():
    cart = session.get("cart", {})
    books = Book.query.filter(Book.id.in_(cart.keys())).all()
    return render_template("cart.html", books=books, cart=cart)
```

---

## 7) Review Creation (With Ownership Checks)

```python
@app.route("/books/<int:book_id>/reviews", methods=["POST"])
@login_required
def add_review(book_id):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            user=current_user,
            book_id=book_id,
            rating=form.rating.data,
            text=form.text.data,
        )
        db.session.add(review)
        db.session.commit()
        return redirect(url_for("book_detail", book_id=book_id))
```

---

## 8) User Authentication (Register, Login, Logout)

```python
# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html", form=form)


# Logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
```

---

## 9) Error Handlers (404 and 403)

```python
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403
```

---

## 10) Book Detail Page

```python
@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    return render_template("book_detail.html", book=book, reviews=reviews)
```

---

## 11) Search Books

```python
@app.route("/books")
def search_books():
    query = request.args.get("q")
    if query:
        books = Book.query.filter(
            or_(Book.title.contains(query), Book.author.contains(query))
        ).all()
    else:
        books = Book.query.all()
    return render_template("books.html", books=books)
```

---

## 12) Contact Page

```python
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # process form data
        pass
    return render_template("contact.html")
```
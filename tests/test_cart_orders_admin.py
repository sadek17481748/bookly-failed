# Cart, checkout, and admin analytics guards.


def test_cart_requires_login(client, sample_book):
    r = client.get("/cart", follow_redirects=False)
    assert r.status_code == 302


def test_add_to_cart_ok(client, app, sample_book):
    with app.app_context():
        from db import db
        from models import User

        u = User(email="buyer@example.com")
        u.set_password("pw123456")
        db.session.add(u)
        db.session.commit()

    client.post(
        "/login",
        data={"email": "buyer@example.com", "password": "pw123456"},
        follow_redirects=True,
    )

    r = client.post(
        f"/cart/add/{sample_book}",
        data={"quantity": "2"},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"Test Book Alpha" in r.data


def test_checkout_empty_cart_redirects(client, app):
    with app.app_context():
        from db import db
        from models import User

        u = User(email="empty@example.com")
        u.set_password("pw123456")
        db.session.add(u)
        db.session.commit()

    client.post(
        "/login",
        data={"email": "empty@example.com", "password": "pw123456"},
        follow_redirects=True,
    )

    r = client.post("/orders/checkout", follow_redirects=True)
    assert r.status_code == 200
    assert b"cart" in r.data.lower()


def test_admin_analytics_requires_login(client):
    r = client.get("/admin/analytics", follow_redirects=False)
    assert r.status_code == 302


def test_admin_analytics_forbidden_for_normal_user(client, app):
    with app.app_context():
        from db import db
        from models import User

        u = User(email="normie@example.com", is_admin=False)
        u.set_password("pw123456")
        db.session.add(u)
        db.session.commit()

    client.post(
        "/login",
        data={"email": "normie@example.com", "password": "pw123456"},
        follow_redirects=True,
    )

    r = client.get("/admin/analytics")
    assert r.status_code == 403


def test_admin_analytics_ok_for_admin(client, app):
    with app.app_context():
        from db import db
        from models import User

        u = User(email="boss@example.com", is_admin=True)
        u.set_password("pw123456")
        db.session.add(u)
        db.session.commit()

    client.post(
        "/login",
        data={"email": "boss@example.com", "password": "pw123456"},
        follow_redirects=True,
    )

    r = client.get("/admin/analytics")
    assert r.status_code == 200
    assert b"Analytics" in r.data or b"revenue" in r.data.lower()


def test_admin_add_book_requires_login(client):
    r = client.get("/admin/books/new", follow_redirects=False)
    assert r.status_code == 302


def test_admin_add_book_forbidden_for_normal_user(client, app):
    with app.app_context():
        from db import db
        from models import User

        u = User(email="noadmin@example.com", is_admin=False)
        u.set_password("pw123456")
        db.session.add(u)
        db.session.commit()

    client.post(
        "/login",
        data={"email": "noadmin@example.com", "password": "pw123456"},
        follow_redirects=True,
    )

    r = client.get("/admin/books/new")
    assert r.status_code == 403


def test_admin_add_book_ok_for_admin(client, app):
    with app.app_context():
        from db import db
        from models import Book, User

        u = User(email="adder@example.com", is_admin=True)
        u.set_password("pw123456")
        db.session.add(u)
        db.session.commit()

    client.post(
        "/login",
        data={"email": "adder@example.com", "password": "pw123456"},
        follow_redirects=True,
    )

    r = client.get("/admin/books/new")
    assert r.status_code == 200
    assert b"Add a new book" in r.data

    r2 = client.post(
        "/admin/books/new",
        data={
            "title": "Admin Added Book",
            "author": "Admin Author",
            "category": "Admin Category",
            "price": "12.99",
            "description": "Added via admin form.",
            "cover_filename": "",
        },
        follow_redirects=True,
    )
    assert r2.status_code == 200

    with app.app_context():
        created = Book.query.filter_by(title="Admin Added Book", author="Admin Author").first()
        assert created is not None

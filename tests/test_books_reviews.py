# Catalog search, reviews (create requires login).


def test_books_search_param_ok(client, sample_book):
    r = client.get("/books?q=Alpha")
    assert r.status_code == 200
    assert b"Test Book Alpha" in r.data


def test_create_review_requires_login(client, sample_book):
    r = client.post(
        f"/books/{sample_book}/reviews",
        data={"rating": "5", "body": "Great"},
        follow_redirects=False,
    )
    assert r.status_code == 302
    assert "login" in (r.headers.get("Location") or "").lower()


def test_create_review_ok(client, app, sample_book):
    with app.app_context():
        from db import db
        from models import User

        u = User(email="reviewer@example.com")
        u.set_password("pw123456")
        db.session.add(u)
        db.session.commit()

    client.post(
        "/login",
        data={"email": "reviewer@example.com", "password": "pw123456"},
        follow_redirects=True,
    )

    r = client.post(
        f"/books/{sample_book}/reviews",
        data={"rating": "4", "body": "Solid read."},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"Solid read" in r.data

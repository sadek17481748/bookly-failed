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


# Registration, login, logout (Flask-Login session cookie).


def test_register_get_ok(client):
    r = client.get("/register")
    assert r.status_code == 200
    assert b"Create account" in r.data or b"Register" in r.data


def test_login_get_ok(client):
    r = client.get("/login")
    assert r.status_code == 200


def test_register_login_flow(client, app):
    with app.app_context():
        from models import User

        assert User.query.filter_by(email="flow@example.com").first() is None

    r = client.post(
        "/register",
        data={
            "email": "flow@example.com",
            "password": "hunter22pass",
            "password2": "hunter22pass",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200

    client.post("/logout", follow_redirects=True)

    r2 = client.post(
        "/login",
        data={"email": "flow@example.com", "password": "hunter22pass"},
        follow_redirects=True,
    )
    assert r2.status_code == 200


def test_register_password_mismatch(client):
    r = client.post(
        "/register",
        data={
            "email": "bad@example.com",
            "password": "aaa",
            "password2": "bbb",
        },
        follow_redirects=False,
    )
    assert r.status_code == 302


def test_login_bad_password(client, app):
    with app.app_context():
        from db import db
        from models import User

        u = User(email="solo@example.com")
        u.set_password("correcthorse")
        db.session.add(u)
        db.session.commit()

    r = client.post(
        "/login",
        data={"email": "solo@example.com", "password": "wrong"},
        follow_redirects=False,
    )
    assert r.status_code == 302

# Registration, login, logout (Flask-Login session cookie).


def test_register_get_ok(client):
    r = client.get("/register")
    assert r.status_code == 200
    assert b"Create account" in r.data or b"Register" in r.data


def test_login_get_ok(client):
    r = client.get("/login")
    assert r.status_code == 200


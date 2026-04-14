# Smoke tests for pages that do not require a login.


def test_home_ok(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"bookly" in r.data.lower() or b"Find your next" in r.data


def test_contact_ok(client):
    r = client.get("/contact")
    assert r.status_code == 200
    assert b"Contact" in r.data


def test_books_list_empty_ok(client):
    r = client.get("/books")
    assert r.status_code == 200
    assert b"Books" in r.data


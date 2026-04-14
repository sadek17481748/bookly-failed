# Smoke tests for pages that do not require a login.


def test_home_ok(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"bookly" in r.data.lower() or b"Find your next" in r.data



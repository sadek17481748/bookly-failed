# Cart, checkout, and admin analytics guards.


def test_cart_requires_login(client, sample_book):
    r = client.get("/cart", follow_redirects=False)
    assert r.status_code == 302



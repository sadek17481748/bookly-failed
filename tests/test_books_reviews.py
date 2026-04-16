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


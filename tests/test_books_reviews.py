# Catalog search, reviews (create requires login).


def test_books_search_param_ok(client, sample_book):
    r = client.get("/books?q=Alpha")
    assert r.status_code == 200
    assert b"Test Book Alpha" in r.data


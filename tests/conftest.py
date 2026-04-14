# Shared pytest fixtures: in-memory DB + Flask test client.

from __future__ import annotations

import os

# These must exist before `app` is imported (app.py calls create_app() at import time).
os.environ.setdefault("SECRET_KEY", "pytest-secret-not-for-production")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import pytest

from app import app as flask_app
from db import db
from models import Book


@pytest.fixture(scope="function")
def app():
    """Fresh empty schema per test (fast enough for this project size)."""
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
    yield flask_app
    with flask_app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_book(app):
    """One catalog row for detail / cart tests."""
    with app.app_context():
        b = Book(
            title="Test Book Alpha",
            author="Test Author",
            category="Testing",
            price_cents=999,
            description="Synthetic row for automated tests.",
            cover_url=None,
        )
        db.session.add(b)
        db.session.commit()
        bid = b.id
    return bid

-- bookly — PostgreSQL DDL (reference copy).
-- The app normally creates tables via SQLAlchemy (`flask init-db`); this file documents the layout.

-- ---------------------------------------------------------------------------
-- Users (login, admin flag, password hash)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  is_admin BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Book catalog
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS books (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  author VARCHAR(255) NOT NULL,
  category VARCHAR(255) NOT NULL DEFAULT 'Uncategorized',
  price_cents INTEGER NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  cover_url VARCHAR(1024),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Reviews (links user + book)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reviews (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
  rating INTEGER NOT NULL,
  body TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

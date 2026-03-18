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


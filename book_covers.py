# ============================================================
# BOOK COVER URL HELPERS
# - Maps a book title to a stable SVG filename slug
# - Used by seeds so `cover_url` points at static/img/covers/*.svg
# ============================================================

from __future__ import annotations

from pathlib import Path
import re


def slug_for_title(title: str) -> str:
    """Filename slug (ASCII, hyphens) matching generated SVG names."""
    # ================= NORMALISE + STRIP PUNCTUATION =================
    s = title.casefold()
    for ch in (
        "\u2019",
        "\u2018",
        "'",
        "`",
    ):
        s = s.replace(ch, "")
    # ================= KEEP ASCII + DASH SEPARATORS =================
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def cover_static_url(title: str) -> str:
    """URL path served by Flask static (see static/img/covers/*)."""
    # ================= PREFER REAL COVER IMAGES =================
    # If a raster cover exists for this title, use it; otherwise fall back to SVG.
    slug = slug_for_title(title)
    covers_dir = Path(__file__).resolve().parent / "static" / "img" / "covers"

    for ext in (".png", ".jpg", ".jpeg", ".webp", ".svg"):
        if (covers_dir / f"{slug}{ext}").exists():
            return f"/static/img/covers/{slug}{ext}"

    # Should not happen, but keeps a stable URL shape.
    return f"/static/img/covers/{slug}.svg"

# ============================================================
# FLASK CLI COMMANDS
# - init-db: create tables and seed starter catalogue
# - reset-db: drop/recreate tables (development only)
# - make-admin: promote an existing user to admin
# ============================================================

from flask import Flask

from db import db
from models import Book, User

from book_covers import cover_static_url


def register_cli(app: Flask) -> None:
    # ================= CLI REGISTRATION =================
    # Attaches `flask init-db`, `flask reset-db`, `flask make-admin` to this app.

    def _seed_books() -> None:
        # ================= SEED / BACKFILL HELPER =================
        # Inserts starter rows that are missing and back-fills `cover_url`
        # for existing rows (so `flask init-db` can fix older databases).

        # ================= SEED CATALOG =================
        # ORM seed objects (one Book() per title).
        seed_books = [
            Book(
                title="1984",
                author="George Orwell",
                category="Dystopian Fiction",
                price_cents=1499,
                description="A chilling story about surveillance, control, and truth.",
                cover_url=cover_static_url("1984"),
            ),
            Book(
                title="To Kill a Mockingbird",
                author="Harper Lee",
                category="Classic / Historical Fiction",
                price_cents=1599,
                description="A powerful classic about justice and compassion in the American South.",
                cover_url=cover_static_url("To Kill a Mockingbird"),
            ),
            Book(
                title="The Great Gatsby",
                author="F. Scott Fitzgerald",
                category="Classic / Tragedy",
                price_cents=1299,
                description="A tragic tale of wealth, love, and the American Dream.",
                cover_url=cover_static_url("The Great Gatsby"),
            ),
            Book(
                title="Harry Potter and the Sorcerer’s Stone",
                author="J.K. Rowling",
                category="Fantasy",
                price_cents=1799,
                description="A young wizard discovers a world of magic and friendship.",
                cover_url=cover_static_url("Harry Potter and the Sorcerer’s Stone"),
            ),
            Book(
                title="The Lord of the Rings",
                author="J.R.R. Tolkien",
                category="Fantasy",
                price_cents=2499,
                description="An epic journey to destroy a powerful ring and save Middle-earth.",
                cover_url=cover_static_url("The Lord of the Rings"),
            ),
            Book(
                title="The Hobbit",
                author="J.R.R. Tolkien",
                category="Fantasy",
                price_cents=1599,
                description="Bilbo Baggins sets out on an unexpected adventure.",
                cover_url=cover_static_url("The Hobbit"),
            ),
            Book(
                title="Pride and Prejudice",
                author="Jane Austen",
                category="Romance / Classic",
                price_cents=1299,
                description="A witty romance about manners, misunderstanding, and love.",
                cover_url=cover_static_url("Pride and Prejudice"),
            ),
            Book(
                title="The Catcher in the Rye",
                author="J.D. Salinger",
                category="Coming-of-age Fiction",
                price_cents=1399,
                description="A teenager’s candid narration of alienation and growing up.",
                cover_url=cover_static_url("The Catcher in the Rye"),
            ),
            Book(
                title="The Hunger Games",
                author="Suzanne Collins",
                category="Dystopian / Sci-Fi",
                price_cents=1699,
                description="A deadly televised competition sparks rebellion.",
                cover_url=cover_static_url("The Hunger Games"),
            ),
            Book(
                title="Brave New World",
                author="Aldous Huxley",
                category="Dystopian / Sci-Fi",
                price_cents=1499,
                description="A futuristic society built on control, pleasure, and conditioning.",
                cover_url=cover_static_url("Brave New World"),
            ),
            Book(
                title="The Diary of a Young Girl",
                author="Anne Frank",
                category="Biography / Memoir",
                price_cents=1499,
                description="Anne Frank’s moving diary written during World War II.",
                cover_url=cover_static_url("The Diary of a Young Girl"),
            ),
            Book(
                title="Long Walk to Freedom",
                author="Nelson Mandela",
                category="Autobiography",
                price_cents=1999,
                description="Mandela’s autobiography about resilience and justice.",
                cover_url=cover_static_url("Long Walk to Freedom"),
            ),
            Book(
                title="Steve Jobs",
                author="Walter Isaacson",
                category="Biography",
                price_cents=1999,
                description="A biography of Apple co-founder Steve Jobs.",
                cover_url=cover_static_url('Steve Jobs'),
            ),
            Book(
                title="Becoming",
                author="Michelle Obama",
                category="Memoir",
                price_cents=1899,
                description="Michelle Obama’s personal story and journey.",
                cover_url=cover_static_url('Becoming'),
            ),
            Book(
                title="The Wright Brothers",
                author="David McCullough",
                category="Biography",
                price_cents=1799,
                description="The inspiring story of the brothers who invented flight.",
                cover_url=cover_static_url('The Wright Brothers'),
            ),
            Book(
                title="Educated",
                author="Tara Westover",
                category="Memoir",
                price_cents=1799,
                description="A memoir about family, education, and transformation.",
                cover_url=cover_static_url('Educated'),
            ),
            Book(
                title="I Am Malala",
                author="Malala Yousafzai",
                category="Biography / Memoir",
                price_cents=1699,
                description="The story of Malala and the fight for education.",
                cover_url=cover_static_url('I Am Malala'),
            ),
            Book(
                title="The Glass Castle",
                author="Jeannette Walls",
                category="Memoir",
                price_cents=1599,
                description="A memoir of a childhood shaped by poverty and resilience.",
                cover_url=cover_static_url('The Glass Castle'),
            ),
            Book(
                title="Born a Crime",
                author="Trevor Noah",
                category="Memoir / Humor",
                price_cents=1699,
                description="A funny and moving memoir about growing up in South Africa.",
                cover_url=cover_static_url('Born a Crime'),
            ),
            Book(
                title="When Breath Becomes Air",
                author="Paul Kalanithi",
                category="Memoir",
                price_cents=1599,
                description="A reflection on life, death, and meaning by a neurosurgeon.",
                cover_url=cover_static_url('When Breath Becomes Air'),
            ),
            Book(
                title="Dune",
                author="Frank Herbert",
                category="Science Fiction",
                price_cents=1899,
                description="A sci-fi epic of politics, prophecy, and survival on Arrakis.",
                cover_url=cover_static_url('Dune'),
            ),
            Book(
                title="Foundation",
                author="Isaac Asimov",
                category="Science Fiction",
                price_cents=1699,
                description="A classic saga about preserving knowledge in a collapsing empire.",
                cover_url=cover_static_url('Foundation'),
            ),
            Book(
                title="Ender’s Game",
                author="Orson Scott Card",
                category="Science Fiction",
                price_cents=1699,
                description="A gifted child is trained to defend humanity in space war.",
                cover_url=cover_static_url('Ender’s Game'),
            ),
            Book(
                title="The Martian",
                author="Andy Weir",
                category="Science Fiction",
                price_cents=1799,
                description="An astronaut uses science and humor to survive on Mars.",
                cover_url=cover_static_url('The Martian'),
            ),
            Book(
                title="Neuromancer",
                author="William Gibson",
                category="Cyberpunk / Sci-Fi",
                price_cents=1599,
                description="A cyberpunk classic that helped define the genre.",
                cover_url=cover_static_url('Neuromancer'),
            ),
            Book(
                title="Snow Crash",
                author="Neal Stephenson",
                category="Cyberpunk / Sci-Fi",
                price_cents=1699,
                description="A fast-paced cyberpunk adventure in a hyper-connected world.",
                cover_url=cover_static_url('Snow Crash'),
            ),
            Book(
                title="Ready Player One",
                author="Ernest Cline",
                category="Sci-Fi / Adventure",
                price_cents=1599,
                description="A virtual reality treasure hunt packed with pop culture.",
                cover_url=cover_static_url('Ready Player One'),
            ),
            Book(
                title="The Time Machine",
                author="H.G. Wells",
                category="Sci-Fi / Classic",
                price_cents=1199,
                description="A classic story of time travel and the future of humanity.",
                cover_url=cover_static_url('The Time Machine'),
            ),
            Book(
                title="Frankenstein",
                author="Mary Shelley",
                category="Sci-Fi / Gothic",
                price_cents=1199,
                description="A foundational gothic tale about creation and responsibility.",
                cover_url=cover_static_url('Frankenstein'),
            ),
            Book(
                title="Jurassic Park",
                author="Michael Crichton",
                category="Sci-Fi / Thriller",
                price_cents=1699,
                description="A techno-thriller where resurrected dinosaurs go wrong.",
                cover_url=cover_static_url('Jurassic Park'),
            ),
            Book(
                title="The Da Vinci Code",
                author="Dan Brown",
                category="Mystery / Thriller",
                price_cents=1599,
                description="A fast-paced mystery involving secrets, symbols, and history.",
                cover_url=cover_static_url('The Da Vinci Code'),
            ),
            Book(
                title="Gone Girl",
                author="Gillian Flynn",
                category="Thriller / Mystery",
                price_cents=1599,
                description="A twisty thriller about a marriage and a disappearance.",
                cover_url=cover_static_url('Gone Girl'),
            ),
            Book(
                title="Sherlock Holmes: A Study in Scarlet",
                author="Arthur Conan Doyle",
                category="Mystery / Detective",
                price_cents=1099,
                description="The first Sherlock Holmes mystery and introduction to Watson.",
                cover_url=cover_static_url('Sherlock Holmes: A Study in Scarlet'),
            ),
            Book(
                title="The Girl with the Dragon Tattoo",
                author="Stieg Larsson",
                category="Crime / Thriller",
                price_cents=1699,
                description="A dark mystery involving a missing person and hidden crimes.",
                cover_url=cover_static_url('The Girl with the Dragon Tattoo'),
            ),
            Book(
                title="Big Little Lies",
                author="Liane Moriarty",
                category="Mystery / Drama",
                price_cents=1599,
                description="Secrets and drama build to a shocking event.",
                cover_url=cover_static_url('Big Little Lies'),
            ),
            Book(
                title="In the Woods",
                author="Tana French",
                category="Crime / Mystery",
                price_cents=1599,
                description="A detective novel with psychological depth and suspense.",
                cover_url=cover_static_url('In the Woods'),
            ),
            Book(
                title="The Silent Patient",
                author="Alex Michaelides",
                category="Psychological Thriller",
                price_cents=1699,
                description="A therapist tries to uncover why a patient stopped speaking.",
                cover_url=cover_static_url('The Silent Patient'),
            ),
            Book(
                title="And Then There Were None",
                author="Agatha Christie",
                category="Mystery",
                price_cents=1299,
                description="A classic mystery where guests are eliminated one by one.",
                cover_url=cover_static_url('And Then There Were None'),
            ),
            Book(
                title="The Woman in the Window",
                author="A.J. Finn",
                category="Thriller",
                price_cents=1599,
                description="A psychological thriller about what was (or wasn’t) seen.",
                cover_url=cover_static_url('The Woman in the Window'),
            ),
            Book(
                title="The Reversal",
                author="Michael Connelly",
                category="Legal Thriller",
                price_cents=1499,
                description="A legal thriller involving a high-profile reversal case.",
                cover_url=cover_static_url('The Reversal'),
            ),
            Book(
                title="The Alchemist",
                author="Paulo Coelho",
                category="Philosophical Fiction",
                price_cents=1399,
                description="A story about purpose, destiny, and following your dream.",
                cover_url=cover_static_url('The Alchemist'),
            ),
            Book(
                title="Life of Pi",
                author="Yann Martel",
                category="Adventure / Philosophical Fiction",
                price_cents=1499,
                description="A survival story with philosophical and spiritual themes.",
                cover_url=cover_static_url('Life of Pi'),
            ),
            Book(
                title="The Kite Runner",
                author="Khaled Hosseini",
                category="Historical Fiction / Drama",
                price_cents=1599,
                description="A powerful novel about friendship, guilt, and redemption.",
                cover_url=cover_static_url('The Kite Runner'),
            ),
            Book(
                title="A Thousand Splendid Suns",
                author="Khaled Hosseini",
                category="Historical Fiction",
                price_cents=1599,
                description="A moving story of love and resilience across generations.",
                cover_url=cover_static_url('A Thousand Splendid Suns'),
            ),
            Book(
                title="The Book Thief",
                author="Markus Zusak",
                category="Historical Fiction",
                price_cents=1499,
                description="A WWII story narrated by Death, centered on books and hope.",
                cover_url=cover_static_url('The Book Thief'),
            ),
            Book(
                title="The Road",
                author="Cormac McCarthy",
                category="Post-Apocalyptic Fiction",
                price_cents=1499,
                description="A stark journey of survival between father and son.",
                cover_url=cover_static_url('The Road'),
            ),
            Book(
                title="The Fault in Our Stars",
                author="John Green",
                category="Romance / Drama",
                price_cents=1499,
                description="A heartfelt romance about two teens facing illness.",
                cover_url=cover_static_url('The Fault in Our Stars'),
            ),
            Book(
                title="Me Before You",
                author="Jojo Moyes",
                category="Romance / Drama",
                price_cents=1499,
                description="A romance that explores love, choice, and change.",
                cover_url=cover_static_url('Me Before You'),
            ),
            Book(
                title="The Help",
                author="Kathryn Stockett",
                category="Historical Fiction",
                price_cents=1599,
                description="A story of courage and friendship in 1960s Mississippi.",
                cover_url=cover_static_url('The Help'),
            ),
            Book(
                title="Where the Crawdads Sing",
                author="Delia Owens",
                category="Mystery / Drama",
                price_cents=1699,
                description="A mystery and coming-of-age story set in the marshes.",
                cover_url=cover_static_url("Where the Crawdads Sing"),
            ),
        ]

        # ================= APPLY SEED (UPSERT-LIKE) =================
        # - Insert missing books
        # - Back-fill cover_url for existing books if missing
        for seeded in seed_books:
            existing = Book.query.filter_by(title=seeded.title).first()
            if existing is None:
                db.session.add(seeded)
                continue

            # Only back-fill or upgrade cover_url; do not overwrite existing catalog text.
            # If we add real cover images later, this will replace older SVG placeholders.
            if (not existing.cover_url) or (
                existing.cover_url.endswith(".svg") and existing.cover_url != seeded.cover_url
            ):
                existing.cover_url = seeded.cover_url

        db.session.commit()

    @app.cli.command("init-db")
    def init_db() -> None:
        # ================= init-db =================
        # Creates tables from models.py, then seeds if the books table is empty.

        db.create_all()

        _seed_books()

        print("Database initialized.")

    @app.cli.command("reset-db")
    def reset_db() -> None:
        # ================= reset-db =================
        # Wipes all data — used after a model/schema change during development.

        db.drop_all()
        db.create_all()
        _seed_books()
        print("Database reset and seeded.")

    @app.cli.command("make-admin")
    def make_admin() -> None:
        # ================= make-admin =================
        # Sets is_admin=True on an existing user (prompts for email in the terminal).

        email = input("Enter the email to make admin: ").strip().lower()
        if not email:
            print("Email is required.")
            return

        user = User.query.filter_by(email=email).first()
        if user is None:
            print("No user found with that email.")
            return

        user.is_admin = True
        db.session.commit()
        print(f"User '{email}' is now an admin.")


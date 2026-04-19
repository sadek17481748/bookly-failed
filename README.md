# bookly — bookstore (PostgreSQL + HTML + CSS + JavaScript + Python)

## Table of Contents

- [Overview](#overview)
  - [Project goals](#project-goals)
  - [Planning notes (written at project start)](#planning-notes-written-at-project-start)
- [Quick links (assessor)](#quick-links-assessor)
- [Features](#features)
- [User Experience (UX)](#user-experience-ux)
  - [User stories](#user-stories)
- [Wireframes](#wireframes)
- [Design](#design)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Development](#development)
- [Deployment](#deployment)
- [Technical overview](#technical-overview)
  - [Why PostgreSQL is the technical centre of this work](#why-postgresql-is-the-technical-centre-of-this-work)
  - [Request flow overview](#request-flow-overview)
  - [Role of Flask](#role-of-flask)
  - [Project 3 scope vs what this submission demonstrates](#project-3-scope-vs-what-this-submission-demonstrates)
  - [Database (PostgreSQL)](#database-postgresql)
  - [HTML, CSS, JavaScript](#html-css-javascript)
- [Testing and Bugs](#testing-and-bugs)
  - [Manual Testing](#manual-testing)
  - [Automated Testing](#automated-testing)
  - [Testing Summary Table](#testing-summary-table)
  - [Lighthouse Testing](#lighthouse-testing)
  - [HTML, CSS and JS Validation](#html-css-and-js-validation)
- [Sources and references](#sources-and-references)
  - [Feature resources (inspiration & references)](#feature-resources-inspiration--references)
- [Attributions](#attributions)
- [Additional Notes](#additional-notes)
- [Author](#author)

---

## Overview

**bookly** is a web app for browsing books, writing reviews, using a shopping cart, and checking out. Purchases are stored in a **PostgreSQL** database.

The site shows a realistic “small business” workflow:

- Visitors can browse catalog content **read from the database** (not hard-coded pages for each book).
- Registered users can **authenticate** securely (passwords stored as hashes, never plaintext).
- Logged-in users can create and manage **their own** reviews (including **edit** and **delete** with server-side ownership checks).
- Logged-in users can add items to a **cart**, adjust quantities, remove lines, and **check out** so that an **order** and **order line items** are written to Postgres.
- An **admin-only** analytics dashboard reads aggregate data from Postgres (counts, sums, joins) to show revenue, orders, top-selling titles, and category distribution.

### Project goals

- Demonstrate a **relational PostgreSQL** design (users, books, reviews, cart, orders).
- Show clear **end-to-end flows** where DB reads/writes show up in the UI (browse → cart → checkout → orders).
- Implement **auth and permissions** properly (hashed passwords, session login, owner-only review edit/delete, admin-only analytics).
- Keep the project easy to mark by using **server-rendered Flask** and a consistent file structure.

### Planning notes (written at project start)

This is the simple logic and screen plan I would write at the start of building bookly (before coding), to keep the scope clear.

#### Logic flow (simple)

- **Guest visitor**
  - I will let guests browse the catalogue (`/books`) and open book detail pages (`/books/<id>`).
  - When a guest tries to do an account-only action (add to cart, checkout, write a review), I will redirect them to **Login**.

- **Register / login**
  - I will create routes for **Register** (`/register`) and **Login** (`/login`).
  - After login, I will store the session so the site knows who the user is on future requests.

- **Cart**
  - I will store cart items per user in the database so the cart persists (not just in the browser session).
  - Users will be able to add to cart, update quantities, and remove items (`/cart`).

- **Checkout → Orders**
  - I will create a checkout page (`/orders/checkout`) that validates the form, then writes an **Order** and **Order Items** to the database.
  - After checkout, I will clear the user’s cart and show the order in **Orders** (`/orders`).

- **Reviews**
  - Logged-in users will be able to post reviews on a book.
  - Only the owner of a review will be able to edit/delete it (server-side check).

- **Admin analytics**
  - I will add an admin-only dashboard (`/admin/analytics`) to read summary information from the database (counts, totals, top sellers).
  - Non-admin users will see a **403** page when trying to access admin routes.

#### Wireframe plan (what I planned to build)

Based on the routes above, my wireframe plan is:

- **Home (`/`)**: hero + clear calls-to-action (browse books, create account).
- **Books (`/books`)**: searchable grid/list of books (title/author/category/price).
- **Book detail (`/books/<id>`)**: cover + description + add-to-cart + reviews section.
- **Register (`/register`)** and **Login (`/login`)**: card forms with validation messages.
- **Cart (`/cart`)**: list of cart items with update/remove controls and subtotal.
- **Checkout (`/orders/checkout`)**: shipping form + order summary + place order.
- **Orders (`/orders`)**: list of previous orders with totals and line items.
- **Admin analytics (`/admin/analytics`)**: KPIs + tables (recent orders, top books, categories).
- **Admin add book (`/admin/books/new`)**: form to add a new book to the catalogue.
- **Error pages (403/404)**: friendly messages with navigation back to safe pages.

## User Experience (UX)

### Navigation

- **Sticky** top bar with brand link, **Home**, **Books**, **Contact**.
- When logged in: **Cart**, **Orders**, **Logout**; if `is_admin`: **Analytics**.
- When logged out: **Login**, **Register**.
- **Mobile:** hamburger control toggles link visibility; `aria-expanded` updated in JS for accessibility.

### Interaction design

- **Flash messages** after register, login, cart changes, checkout, errors (categories `success` / `error` styled in CSS).
- **Forms** use labels, placeholders where helpful, and `sr-only` labels for compact controls (e.g. quantity on cart rows).
- **Skip link** to `#main` for keyboard users.
- **Confirm** dialog on destructive actions (e.g. delete review) via `data-confirm` in `main.js`.

### Responsive behaviour

- **Best viewed on laptop/desktop:** the catalogue grid, checkout summary, order history, and especially the **admin analytics tables** are easier to read and compare on a wider screen (more items visible at once, less scrolling).
- **Phone/tablet support:** the site was adjusted to be usable on smaller screens (responsive CSS breakpoints stack multi-column layouts into a single column, the book detail page collapses, the footer becomes one column, and the navigation switches to a hamburger menu).

#### Responsiveness testing evidence

![Responsive testing on mobile, tablet and laptop](docs/images/validation/responsive-test-devices.png)

### User stories

**First-time / guest user**

- As a guest, I want to land on a clear home page so I understand what the site does and what I can do next.
- As a guest, I want to browse the catalogue so I can explore what books are available before making an account.
- As a guest, I want to search by title/author so I can find a specific book quickly.
- As a guest, I want to open a book detail page so I can read the description and existing reviews before deciding whether to register.
- As a guest, I want to see a clear message when I try to access a protected feature (cart, orders, reviews) so I know I need to log in.

**Registered / returning user**

- As a user, I want to register and log in so I can access features that require an account (reviews, cart, checkout, orders).
- As a user, I want to add books to my cart and adjust quantities so I can control my order without starting over.
- As a user, I want the cart total to update correctly when I change quantities so I can trust the checkout amount.
- As a user, I want to check out so my purchase is saved as an order (with order items) in the database.
- As a user, I want to view my order history so I can confirm what I bought after checkout.
- As a user, I want to create reviews with a rating and text so I can share feedback on books I read.
- As a user, I want to edit/delete **my own** reviews so I can correct mistakes or remove outdated feedback.
- As a user, I want to be prevented from editing/deleting other people’s reviews so the site feels fair and secure.

**Admin**

- As an admin, I want to view the analytics dashboard so I can monitor revenue, orders, and top-selling books.
- As an admin, I want to see a category breakdown so I can understand the shape of the catalogue at a glance.
- As an admin, I want to add a new book to the catalogue (including a category and cover) so I can expand inventory without touching the database directly.
- As an admin, I want non-admin users to be blocked from admin pages so sensitive business information is protected.

### Target audience & user stories

The site is aimed at **readers** who want a simple way to browse a small catalogue, check book details, read/write reviews, and place an order using a lightweight checkout flow. It is also aimed at a **store admin** who needs quick visibility of what is happening in the store (revenue, order volume, top sellers, and category distribution) without exporting data or running SQL manually.

In practice, I thought about three “audience groups” while building and testing:

- **Guest visitors**: explore the catalogue and understand the value of the site without being forced to create an account immediately.
- **Registered customers**: complete the core journey (browse → cart → checkout → orders) and manage their own reviews.
- **Admin user**: manage the catalogue (add books) and review store performance using the analytics dashboard.

The user stories above are the ones I used to guide feature scope and testing. They map directly to the live routes and the database flows (catalogue read, review write, cart write, order + order items write, and analytics aggregates).

---

## Features

### Public browsing

- **Home** page with calls-to-action (browse, register).
- **Book catalog** with optional **search** (`?q=`) over title and author (case-insensitive `ILIKE` in SQLAlchemy → Postgres).
- **Book detail** with description, optional cover image path, cart form (if logged in), and reviews.

### Authentication

- **Register**, **login**, **logout** (Flask-Login).
- Passwords stored with **Werkzeug** hashing (`set_password` / `check_password` on `User`).

### Reviews (CRUD)

- **Create** and **read** reviews on a book; **update** and **delete** only for the **owning** user (checked in `books.py`).
- Reviews are stored with `user_id` and `book_id` foreign keys.

### Cart & checkout

- Add to cart (merge quantity if the same book is already in the cart).
- Update quantity or remove a line.
- **Checkout** collects minimal shipping fields, creates an **order** + **order items**, then **clears the cart** (no external payment gateway—orders are persisted for coursework realism).

### Admin analytics

- **Admin-only** route (`is_admin` on `users`).
- Dashboard metrics from SQL aggregates: revenue, order counts, top sellers, books per category, recent orders.

### Book covers

- Generated **SVG** artwork per seeded title lives under `static/img/covers/`.
- `book_covers.py` maps each title to a stable URL; seeds set `cover_url` so templates can render `<img src="...">`.

---

## Wireframes

Low-fidelity wireframes for bookly are in this repository as a single PDF:

- **[`docs/wireframe-bookly.pdf`](docs/wireframe-bookly.pdf)** — planning layouts for the main flows (home, catalogue, book detail, auth, cart/checkout, orders, admin). The screens map to the live routes: **Home** (`/`), **Books** (`/books`), **Book detail** (`/books/<id>`), **Login / Register**, **Cart**, **Checkout**, **Orders**, and **Admin analytics** (`/admin/analytics`).

Any extra Figma links or annotated screenshots I used only in the written report stay in the **coursework appendix**; this PDF is the main wireframe file in the repo.

### Wireframe description (screen-by-screen)

The PDF wireframe is intentionally low fidelity (boxes, labels, and simple components), but it still captures the **layout decisions** and the main **user actions** for each route.

#### Global layout used across screens

- **Header navigation**: logo on the left and the main links on the right (**Home**, **Books**, **Contact**).
- **Auth-aware nav**:
  - When logged out: **Login**, **Register**
  - When logged in: **Cart**, **Orders**, **Logout** (and **Analytics** for admin users)
- **Footer**: quick links (**Contact us**, **Browse books**, **Sitemap**) plus social icons.

#### Home (`/`)

- A hero panel with the primary message (“Discover your next favourite book / Find your next great read”) and two clear calls to action:
  - **Browse books**
  - **Create account**
- Supporting feature cards to preview core functionality (reviews + checkout).

#### Books catalogue (`/books`)

- Page heading (“Our books / Books list”) and a **search bar** (“Search by title or author”).
- A **grid of book cards**, each showing:
  - title, author, category, price
  - an action to **view details** and/or **add to cart** (depending on auth state in the live app).

#### Book detail (`/books/<id>`)

- A split layout with:
  - **Cover image** panel
  - **Book metadata** (title, author, category, price) and a longer description
- A quantity selector and **Add to cart** action (shown for logged-in users in the real UI).
- Reviews section:
  - List of reviews (reviewer email, timestamp, rating, body)
  - Owner controls for edit/delete (represented in the wireframe as buttons alongside reviews).

#### Login (`/login`)

- A compact “card” form with:
  - Email input
  - Password input
  - Login button
  - Link to Register

#### Register (`/register`)

- A matching “card” form with:
  - Email input
  - Password input
  - Confirm password input
  - Register button
  - Link to Login

#### Cart (`/cart`)

- A list/table of cart items with:
  - title, unit price, quantity input
  - **Update** and **Remove** actions per line
- An order summary area showing a subtotal and a clear **Checkout** button.

#### Checkout (`/orders/checkout`)

- A two-column layout:
  - Left: shipping information inputs and a **Place order** button
  - Right: an **order summary** (items, quantities, totals)

#### Orders (`/orders`)

- A list of previous orders (order IDs / timestamps), with the intention that an order can be expanded to show line items and totals.

#### Admin analytics (`/admin/analytics`)

- An admin-only dashboard screen with:
  - KPI summary cards (sales, books, users, new orders)
  - Category breakdown and top sellers
  - Recent orders table
  - A clear admin call-to-action: **Add new book**

#### Admin add book (`/admin/books/new`)

- A form layout for adding to the catalogue, including:
  - title, author, category, price
  - cover image selector
  - description
  - submit button

#### Error pages (403 / 404)

- **404**: a friendly “Page not found” message with buttons to return home or browse books.
- **403**: a clear “Forbidden” message with a back-home action.

---

## Website build process and planning (milestones)

This section summarises **how bookly was built**, in the order features were implemented, and how the scope evolved as I worked through the coursework requirements.

### Foundation completion — **28/03**

I started by building the foundation so every later feature had a stable base:

- **Project setup**: virtual environment, dependencies, and a clean Flask project structure.
- **Configuration**: environment-based settings (`SECRET_KEY`, `DATABASE_URL`) so the same code could run locally and in a hosted environment. (AI)
- **Database first**: a PostgreSQL schema that reflects the core entities and relationships (`users`, `books`, `reviews`, `cart_items`, `orders`, `order_items`) with sensible constraints (foreign keys and uniqueness where needed).
- **Bootstrap commands and seed data**: a repeatable way to initialise the schema and seed a starter catalogue so pages were never “empty by default”. (AI)
- **Shared UI shell**: `base.html` with navigation, flash messages, and consistent layout, plus a first pass of CSS variables and reusable components.

The practical reason for doing this first was personal experience: once the database and layout are stable, every new page becomes “connect the route to the template to the query”, instead of reinventing structure on every screen.(AI)

### Milestone 1 — **31/03** (public pages + shared layout)

This milestone focused on getting the public-facing shell working end-to-end:

- **Home** and **Contact** pages built against the wireframe.
- A consistent navigation experience across pages (logged out experience first).
- Early error pages (especially **403/404**) so the site behaved clearly while routes were still being added.

### Milestone 2 — **05/04** (catalogue)

Once the shell was working, I moved onto the first database-driven feature:

- **Books list** (`/books`) populated from the database rather than static HTML.
- **Book detail** (`/books/<id>`) with price, description, and cover rendering.
- A simple **search** experience (`?q=`) to demonstrate database filtering.
- Catalogue seeding and cover URLs so the UI looked complete and consistent.

### Milestone 3 — **10/04** (authentication)

At this point scope shifted from “pages” to “user actions”:

- **Register / login / logout** implemented with hashed passwords and session management.
- Navigation updated based on authentication state (cart/orders only appear when logged in).
- Protected routes added so guest users are redirected away from actions that require an account.

### Milestone 4 — **13/04** (reviews)

Reviews were the first feature that required a mix of database relationships and security checks:

- Logged-in users can **create** reviews linked by foreign keys to both the user and the book.
- Reviews display on the book detail page.
- **Edit and delete** are restricted to the review owner with server-side checks (not only template logic).

### Milestone 5 — **16/04** (cart)

The cart is implemented as a database feature (not a session-only cart), which made scope and data modelling more important:

- Add-to-cart writes to `cart_items` and merges quantity using a uniqueness rule for one row per (user, book).
- The cart page supports quantity updates and removals with totals calculated from book prices.
- Edge cases handled (empty cart, invalid quantities) so the checkout flow would not be fragile later.

### Milestone 6 — **20/04** (checkout + orders)

This milestone turned “basket data” into “transaction history”:

- Checkout form added (minimal shipping/contact fields for coursework realism).
- Submitting checkout creates an `orders` row and multiple `order_items` rows, then clears the cart for that user.
- Orders history added so users can view what they purchased after checkout.

### Milestone 7 — **25/04** (admin analytics + final integration)

Admin analytics was the last major feature because it depends on the rest of the data model being correct:

- Admin-only route protection with a clear **403** for non-admin users.
- Dashboard queries based on aggregates and joins (revenue, order counts, top books, categories).
- A final integration pass to make flows consistent (navigation, flash messaging, and layout across templates).

### Testing and final foundation pass — **25/04**

Testing was completed alongside feature work, but the final day was a dedicated pass to make sure everything was coherent:

- **Automated testing**: pytest suite for key routes and behaviours using a fast in-memory database for repeatable runs.
- **Manual testing**: end-to-end walkthroughs on PostgreSQL (browse → auth → review → cart → checkout → orders), plus admin access checks.
- **Scope reflection**: the largest scope risks were multi-table writes (checkout) and role/ownership enforcement (reviews + admin). Those were the areas I revisited most during the final testing pass because they are easiest to “seem fine” until you try edge cases.

### Personal reflection (time constraints and improved time/communication plan)

From personal experience, project time constraints can change quickly. During this project I was **heavily delayed by personal issues**, which reduced the amount of uninterrupted time I had for development and testing. Even though the core features were completed, the delay meant I had to compress work into fewer sessions, which increases the risk of mistakes and makes progress harder to track.

In future projects, to manage my time and communication better, I would take the following steps.

#### What I would do differently next time

- **Start with a realistic schedule and visible checkpoints**
  - Break the project into small deliverables (foundation, catalogue, auth, reviews, cart, checkout, admin, testing).
  - Set short checkpoints (every 2–3 days) so progress is measurable even when time is limited.
- **Timebox work sessions and protect “core hours”**
  - Plan focused sessions (for example 60–90 minutes) with a single goal (one route, one feature, or one bug).
  - Reserve dedicated time for testing and bug fixing rather than leaving it to the end.
- **Prioritise core functionality first (MVP first)**
  - Build the “must-have” user journey early: browse → login → cart → checkout → orders.
  - Treat admin analytics and extra polish as optional until the main flow is stable.
- **Track decisions and changes as I go**
  - Keep short notes after each session (what was done, what broke, what is next).
  - Record database changes and why they were made so I do not lose time re-learning decisions later.
- **Communicate earlier when delays happen**
  - If I hit a personal issue or a schedule slip, I would communicate it earlier rather than trying to recover silently.
  - Share a revised plan (what will be completed first, and what may be reduced) so expectations stay clear.
- **Reduce risk by testing continuously**
  - Run automated tests regularly (not only at the end).
  - Do quick manual checks after each major feature (especially multi-table writes like checkout and role/ownership rules).

#### What I learned

This project reinforced that the biggest risk under time pressure is not writing code—it is losing structure: forgetting what changed, delaying testing, and trying to complete too many features at once. A clearer schedule, earlier communication, and smaller planned deliverables would make future projects more controlled and less stressful, even if delays happen.

#### Planned but not completed (time constraint)

Late in development, I planned a small admin improvement: a **“Complete order”** button on the admin side (so an admin could mark an order as completed after checkout). The idea came from watching extra e-commerce tutorials and thinking about how a real store would track order status, but I did not have enough time to implement it properly before submission.

In a future iteration, I would add an `order_status` field (for example: Pending → Completed), show it on the admin dashboard, and only allow status changes for admin users with server-side validation. (AI)

---

## Design

### Visual language

- **Dark theme** with CSS variables (`--bg`, `--panel`, `--text`, `--brand`, `--danger`, etc.) in `static/css/styles.css` for consistent colour and spacing.
- **Gradients** on hero and buttons for depth; **cards** with subtle borders and shadows for content grouping.
- **Typography:** system UI stack (`ui-sans-serif`, `system-ui`, …) for fast loading and native feel.

### Colour scheme (and why)

The site uses a **dark, high-contrast** palette to keep long reading sessions comfortable and to make book covers and cards stand out clearly.

- **Background (`--bg`)**: deep navy used as the base canvas so content panels feel separated without heavy borders.
- **Panels (`--panel`)**: slightly lighter navy for cards and sections to create depth while staying consistent with the dark theme.
- **Text (`--text`) + muted text (`--muted`)**: bright off-white for readability, with a muted variant for secondary information (author names, timestamps, hints).
- **Primary brand (`--brand`)**: purple accent for primary actions and key highlights (buttons, links) to give the UI a recognisable identity.
- **Secondary accent (`--brand2`)**: green accent used sparingly to add contrast in gradients and to avoid a single-colour interface.
- **Danger (`--danger`)**: pink/red accent reserved for destructive actions (delete/remove) so risk actions are visually obvious.

These choices are implemented as CSS variables at the top of `static/css/styles.css` so the palette is consistent across the whole site and easy to adjust in one place.

### Layout

- **Max content width** (`--max`) with horizontal padding so lines do not stretch too wide on large monitors.
- **CSS Grid** for book grids (two/three columns, collapsing on small viewports).
- **Admin dashboard:** stat tiles + scrollable table for “top books”.

### Imagery

- **Covers:** SVG files under `static/img/covers/` (title + author on gradient) to avoid copyright issues with publisher jacket scans while still filling the layout.

### Accessibility choices

- Skip link, `aria-live` on flash stack, `aria-label` / `aria-expanded` where applicable, visible focus on skip link.

---

## Technologies Used

### Languages

- **Python** — application logic, ORM, routing.
- **HTML** — structure via Jinja2 templates.
- **CSS** — layout and theme.
- **JavaScript** — small client behaviours only.

### Frameworks & libraries

| Piece | Role |
|-------|------|
| **Flask** | Web framework, routing, templates |
| **Flask-Login** | Session-based authentication |
| **Flask-SQLAlchemy** | ORM + session management to PostgreSQL |
| **psycopg2** (binary) | PostgreSQL driver in `DATABASE_URL` |
| **python-dotenv** | Load `.env` locally |
| **gunicorn** | Production WSGI server (Heroku `Procfile`) |
| **pytest** | Automated tests (`tests/`) |

**Frontend libraries note:** No UI framework such as **Bootstrap** was used. The UI is custom CSS in `static/css/styles.css` and a small amount of vanilla JavaScript in `static/js/main.js` (no jQuery).

### Tools

| Tool | Used for |
|------|----------|
| **Git** | Version control |
| **PostgreSQL / psql** | Local database, ad-hoc SQL checks |
| **VS Code** | Editing and integrated terminal |
| **Heroku CLI** | Deploy, logs, `heroku run` for `init-db` |
| **Chrome DevTools** | Network tab, responsive mode, Lighthouse |

---

## File Structure

> Paths are relative to the project root (`bookly-final/`).

| Path | Description |
|------|-------------|
| `app.py` | Flask app factory, extensions, blueprint registration, `/`, `/contact`, 403 handler |
| `book_covers.py` | Slug + `/static/img/covers/...` URL helper for seeded covers |
| `config.py` | `SECRET_KEY`, `DATABASE_URL`, SQLAlchemy flags from environment |
| `db.py` | Shared SQLAlchemy `db` instance |
| `models.py` | ORM models (users, books, reviews, cart, orders) |
| `auth.py` | Register / login / logout blueprint |
| `books.py` | Catalog, detail, review CRUD blueprint |
| `cart.py` | Cart blueprint |
| `orders.py` | Orders + checkout blueprint |
| `admin.py` | Admin analytics blueprint + `admin_required` decorator |
| `cli.py` | `flask init-db`, `reset-db`, `make-admin`; seeds books and back-fills `cover_url` values |
| `templates/` | Jinja2 HTML (includes admin pages) |
| `templates/admin_add_book.html` | Admin-only “Add book” form (category + cover selection) |
| `static/css/styles.css` | Site styles |
| `static/js/main.js` | Nav toggle + confirm helper |
| `static/img/covers/` | Cover assets used by the catalogue (SVG placeholders + any added raster covers) |
| `schema.sql` | Reference DDL for PostgreSQL |
| `seed_books.sql` | Optional bulk SQL seed (includes `cover_url` paths) |
| `tests/` | Pytest suite + `conftest.py` (in-memory SQLite for CI speed) |
| `pytest.ini` | Pytest discovery settings |
| `requirements.txt` | Python dependencies |
| `Procfile` / `runtime.txt` | Heroku process + Python version |
| `.env.example` | Documents required env vars (no secrets) |
| `.gitignore` | Ignores `.env`, `.venv`, `__pycache__`, etc. |
| `docs/devlog.md` | (Removed) dev notes were merged into `README.md` |
| `docs/testing.md` | (Removed) testing notes were merged into `README.md` |
| `docs/legacy-code.md` | Small “before → after” code snapshots for assessor review |
| `docs/wireframe-bookly.pdf` | Wireframes (PDF) for main screens and flows |
| `docs/images/manual-testing/` | Manual testing evidence screenshots used in the testing table |
| `docs/images/validation/` | Evidence screenshots (Lighthouse, W3C validators, JSHint, responsiveness, 404) |
| `tools/` | One-off helper scripts used during development (not part of the running app) |

---

## Development

### Prerequisites

- **Python 3.11+** (Heroku pin in `runtime.txt`).
- **PostgreSQL** installed and running locally (e.g. Homebrew Postgres on macOS).

### Environment setup
```bash
cd /path/to/bookly-final
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

In `.env` I set:

- **`SECRET_KEY`** — a long random string for sessions.
- **`DATABASE_URL`** — SQLAlchemy URL for Postgres, for example:

```text
postgresql+psycopg2://bookly_user:change_me@localhost:5432/bookly_db
```

Example SQL to create a matching role and database (names line up with the example URL above):

```sql
CREATE USER bookly_user WITH PASSWORD 'change_me';
CREATE DATABASE bookly_db OWNER bookly_user;
```

### Initialise the database (PostgreSQL)

```bash
source .venv/bin/activate
python -m flask --app app.py init-db
```

This creates tables from `models.py` and seeds books if the catalog is empty.

### Run the app locally

```bash
source .venv/bin/activate
python -m flask --app app.py run --debug
```

The app served at `http://127.0.0.1:5000` during local runs.

### Troubleshooting (local Postgres setup)

- **`password authentication failed for user ...`**
  - This usually means `DATABASE_URL` in `.env` still has placeholder values or the Postgres user password does not match.
  - Fix by updating `.env` to a real connection string and (re)setting the user password in Postgres, for example:

```sql
ALTER USER bookly_user WITH PASSWORD 'bookly_pass';
```

- **Commands typed inside `psql` by mistake**
  - If the prompt looks like `postgres=#` or `postgres-#`, you are inside Postgres interactive mode.
  - Exit with `\q` to return to the normal terminal prompt before running:
    - `python -m flask --app app.py init-db`
    - `python -m flask --app app.py run --debug`

### Promote an admin user

After I registered a user in the browser:

```bash
python -m flask --app app.py make-admin
```

The command prompts for an email; I used the account I wanted to promote so `is_admin` is set and `/admin/analytics` unlocks.

### Assessor / invigilator login (analytics access)

To make marking simpler, I created a dedicated admin account for the analytics dashboard:

- **Email:** `analytics@testemail.com`
- **Password:** `test123`

After logging in, the admin analytics dashboard is available at **`/admin/analytics`**.

**Note (live Heroku app):** The Heroku deployment uses its own Postgres database, so the account must be **registered on the live site** and then promoted to admin (set `users.is_admin = true`). This can be done using `heroku pg:psql` or by running the existing CLI command (`make-admin`) against the Heroku app.

## Quick links (assessor)

- **Repository (README / code)**: [`sadek17481748/bookly`](https://github.com/sadek17481748/bookly-failed)
- **Wireframes section (README anchor)**: [Wireframes](https://github.com/sadek17481748/bookly-failed#wireframes)
- **Live app (Heroku)**: [`bookly-final-98e88d5d388e.herokuapp.com`](https://bookly-final-98e88d5d388e.herokuapp.com/)
- **Live app login page**: [Login](https://bookly-final-98e88d5d388e.herokuapp.com/login)
- **Analytics dashboard (admin-only)**: [`/admin/analytics`](https://bookly-final-98e88d5d388e.herokuapp.com/admin/analytics) — shows revenue, orders, top sellers, and catalogue breakdown (requires the assessor admin login).
- **Assessor analytics login**: `analytics@testemail.com` / `test123` — admin account for accessing the analytics dashboard on the live site.
- **Bug tracker (GitHub Project board)**: [`github.com/users/sadek17481748/projects/6`](https://github.com/users/sadek17481748/projects/6)
- **GitHub Pages (documentation site)**: [`sadek17481748.github.io/bookly`](https://sadek17481748.github.io/bookly/)
- **Closed issues (progress log)**: [GitHub Issues (closed)](https://github.com/sadek17481748/bookly-failed/issues?q=is%3Aissue%20state%3Aclosed)

## Key UI screenshots (assessor)

Screenshots are shown below so key screens are visible directly in this README.

### Home

![Home page](docs/images/manual-testing/01-home.png)

### Books

![Books list page](docs/images/manual-testing/03-books-list.png)

### Contact

![Contact page](docs/images/manual-testing/02-contact.png)

### Login

![Login page](docs/images/manual-testing/08-login-success.png)

### Register

![Register page](docs/images/manual-testing/06a-register-form.png)

### Analytics (admin)

![Analytics dashboard](docs/images/manual-testing/21-analytics-admin.png)

---

### Automated tests (no Postgres required for pytest)

```bash
source .venv/bin/activate
pytest -v
```

Tests use **SQLite in-memory** via `tests/conftest.py` so they run quickly; I still demonstrated PostgreSQL using the steps above. A feature → test mapping is included in the Automated testing section below.

---

## Deployment

I deployed bookly to Heroku and used Heroku Postgres for the production database.

### Heroku deployment (step-by-step)

**Install and login (local machine):**

```bash
brew tap heroku/brew && brew install heroku
heroku login
```

**Create/link the Heroku app:**

```bash
cd /path/to/bookly-final
heroku create bookly-final
heroku git:remote -a bookly-final
```

**Add a managed Postgres database (sets `DATABASE_URL`):**

```bash
heroku addons:create heroku-postgresql:essential-0 -a bookly-final
```

**Set required config vars:**

```bash
heroku config:set SECRET_KEY="a-long-random-string" -a bookly-final
```

**Deploy code and initialise the database (create tables + seed):**

```bash
git push heroku main
heroku run -a bookly-final -- python3 -m flask --app app.py init-db
heroku open -a bookly-final
```

**Production notes:**

- `Procfile` runs the app with **Gunicorn** (`gunicorn app:app`).
- Heroku provides `DATABASE_URL` in the `postgres://...` form; the app normalises this to `postgresql://...` for SQLAlchemy compatibility in `config.py`.
- During deployment I used `heroku logs --tail -a bookly-final` to diagnose startup issues.

**Live site URL (Heroku):**

- `https://bookly-final-98e88d5d388e.herokuapp.com/`

### GitHub repository + Pages

- I created the GitHub repository and added the project documentation (`README.md`).
- To publish the documentation on GitHub Pages, I opened **Settings → Pages**, selected **Deploy from a branch**, chose **`main`** as the source, and saved to generate the Pages site.
- I also used GitHub **Issues** to log issues and user stories, and to track progress throughout development.

### How I committed changes to GitHub (workflow used)

During development I used a simple Git workflow so changes were traceable and easy to review:

- I checked what changed with `git status` and `git diff`.
- I staged the files I wanted in the commit with `git add ...`.
- I created a commit with a short message describing what changed and why.
- I pushed commits to GitHub so the repository stayed up to date.

Typical commands I used:

```bash
git status
git diff
git add README.md
git commit -m "docs(readme): update testing evidence"
git push origin main
```

Where changes affected both documentation and the app itself, I kept commits separate so it was obvious what was “README/docs” and what was “code changes”.

---

## Technical overview

### Why PostgreSQL is the technical centre of this work

PostgreSQL is a core part of the project:

- **Connection:** the app reads `DATABASE_URL` from the environment (`config.py`, `.env.example`). In development this pointed at a **local Postgres** instance; on Heroku it used the **managed Postgres** add-on URL.
- **Integrity:** foreign keys tie reviews to users and books, cart lines to users and books, order items to orders and books. `schema.sql` lists the same structure for reference and marking.
- **Meaningful writes:** checkout creates an `orders` row and multiple `order_items` rows, then deletes `cart_items` for that user—i.e. a **multi-table write** I verified in `psql` and other SQL clients during development.
- **Read patterns:** the admin dashboard uses **aggregations** (`COUNT`, `SUM`, `GROUP BY`, joins) executed against real tables—exactly the kind of SQL competence Project 3 is meant to evidence, surfaced through the UI.

Automated tests in `tests/` use **SQLite in-memory** only so `pytest` runs quickly **without** Postgres on the machine running CI. For marking and demos I still ran the app against **PostgreSQL** as described in [Development](#development).

### Request flow overview

1. The browser requests a URL (e.g. `/books`).
2. Flask maps the URL to a **view function** in a blueprint (`books.py`, `cart.py`, etc.).
3. The view uses **SQLAlchemy** to query or change rows in **PostgreSQL** (via `DATABASE_URL`).
4. Flask renders a **Jinja2** template and injects the results (e.g. `books`, `reviews`).
5. The server returns **HTML**; the browser requests **static** assets (`styles.css`, `main.js`).
6. Small behaviours (mobile nav toggle, `data-confirm` on delete) are handled in **JavaScript** without replacing server-side validation.

This is **server-side rendering**, not a single-page React/Vue app: most HTML is produced on the server, which keeps the project understandable while still being “full stack” in the sense of **HTTP + app + database**.

### Role of Flask

Flask provides the **web layer** between the user and PostgreSQL:

- **Routing:** maps paths like `/`, `/books`, `/cart`, `/orders/checkout` to Python functions.
- **HTTP verbs:** distinguishes **GET** (show form or page) from **POST** (submit form, mutate data).
- **Sessions / auth:** Flask-Login loads the current user from the session cookie and ties actions to `users.id` in Postgres.
- **Templates:** connects each response to a file under `templates/`.
- **Blueprints:** splits features into `auth.py`, `books.py`, `cart.py`, `orders.py`, `admin.py` so the codebase stays readable.

### Database (PostgreSQL)

PostgreSQL stores:

- **Users** (email, password hash, admin flag, timestamps).
- **Books** (title, author, category, price in cents, description, optional `cover_url`).
- **Reviews** (rating, body, links to user and book).
- **Cart items** (per user and book, quantity; unique constraint so one row merges quantities).
- **Orders** and **order items** (order header + line items with **unit price snapshot** in cents).

SQLAlchemy maps Python classes in `models.py` to these tables. **`flask init-db`** calls `db.create_all()` so the live schema matches the models (`cli.py`). **`schema.sql`** is a human-readable duplicate of the layout for documentation and external review.

### Project 3 scope vs what this submission demonstrates

For **Project 3**, the emphasis is on **PostgreSQL**—designing tables, relationships, and queries—and demonstrating that data in a working project.

While building bookly, I watched a range of tutorials and walkthroughs (Flask + database projects). As a result, I included a few extra “real app” steps that were not strictly required by the brief, because they helped me complete the overall logic of the site and make the database work easier to demonstrate end-to-end.

| Typical Project 3 focus | What bookly adds (and why) |
|-------------------------|----------------------------|
| SQL scripts, ER thinking, maybe a thin UI | **End-to-end paths**: browser → Flask routes → SQLAlchemy → **PostgreSQL** → HTML response. That makes the database work **visible and testable** as part of a real use case (browse → cart → checkout → orders). |
| Less emphasis on auth, sessions, deployment | **Flask-Login** sessions, **environment-based configuration**, and a **Heroku-style** deployment story so Postgres is not “theory only” but runnable **locally and** on a hosted database. |

**Why this still fits the marking criteria**

1. **PostgreSQL remains the source of truth.** Users, books, reviews, cart rows, orders, and order items all live in Postgres. The ORM generates SQL; constraints (foreign keys, uniqueness on cart lines) match standard relational design taught on the course.
2. **A thin static page** can show a `SELECT` result, but it does not demonstrate **transactions across steps** (cart updates, checkout clearing the cart while inserting orders) or **authorization** (only the review owner can delete). Those behaviours need **application logic** tied to the database.
3. **Separation of concerns is still clear:** `schema.sql` documents the DDL; `models.py` mirrors it for SQLAlchemy; `books.py`, `cart.py`, `orders.py` show **which HTTP actions cause which writes** to Postgres.

For assessment, **`schema.sql`** and the **`models.py` ↔ table mapping** document the relational design and local setup. The Flask routes and blueprints show **how** that PostgreSQL design is exercised in practice (browse, cart, checkout, admin reads).

### HTML, CSS, JavaScript

- **HTML / Jinja2** under `templates/` builds pages and loops (e.g. book grid, review list).
- **CSS** in `static/css/styles.css` defines layout, dark theme, responsive grids, forms, and admin tables.
- **JavaScript** in `static/js/main.js` adds progressive enhancements (nav toggle, confirm before destructive POSTs). **Security rules stay on the server** (e.g. “only delete your own review” is enforced in Python, not only in JS).

### Why this approach?

Server-rendered Flask keeps the database work clear: every important screen is backed by a query or a write to **PostgreSQL**. This matches Project 3 learning outcomes while still being a complete small app.

---

## Testing and Bugs

### Manual testing

I complemented automated tests with manual runs in the browser, recording **what I did**, **what I expected**, and **what happened**. The table below is the checklist I used; I filled **Pass/Fail**, **Notes**, and captured screenshots in `docs/images/manual-testing/`.

| # | Area | Step | Expected | Pass/Fail | Notes | Screenshot evidence |
|---|------|------|----------|-----------|-------|-------------------|
| 1 | Public | Open `/` | Home loads; branding and hero visible | Pass |  | [01-home](docs/images/manual-testing/01-home.png) |
| 2 | Public | Open `/contact` | Contact content loads | Pass |  | [02-contact](docs/images/manual-testing/02-contact.png) |
| 3 | Public | Open `/books` | Catalog or empty state loads | Pass |  | [03-books-list](docs/images/manual-testing/03-books-list.png) |
| 4 | Public | Use search `?q=` with a known title | Matching books appear | Pass |  | [04-search](docs/images/manual-testing/04-search.png)<br>[04b-search-no-results](docs/images/manual-testing/04b-search-no-results.png) |
| 5 | Public | Open a book detail URL | Title, author, price, description | Pass |  | [05-book-detail](docs/images/manual-testing/05-book-detail.png) |
| 6 | Auth | Register a new user | Redirect to books; flash success | Pass |  | [06a-register-form](docs/images/manual-testing/06a-register-form.png)<br>[06-register-success](docs/images/manual-testing/06-register-success.png) |
| 7 | Auth | On Register, enter an invalid email format | Browser validation blocks submit; user is prompted to enter a valid email | Pass |  | [24-register-email-required](docs/images/manual-testing/24-register-email-required.png) |
| 8 | Auth | On Register, enter a password under 6 characters | Browser validation prompts “Use at least 6 characters” | Pass |  | [25-register-password-min-length](docs/images/manual-testing/25-register-password-min-length.png) |
| 9 | Auth | Register with mismatched passwords | Error message shown; account not created | Pass |  | [26-register-passwords-dont-match](docs/images/manual-testing/26-register-passwords-dont-match.png) |
| 10 | Auth | Log out | Session cleared; home or login | Pass |  | [07-logout](docs/images/manual-testing/07-logout.png) |
| 11 | Auth | Log in with correct password | Redirect; flash success | Pass |  | [08-login-success](docs/images/manual-testing/08-login-success.png) |
| 12 | Auth | Log in with wrong password | Stays on login; flash error | Pass |  | [09-login-fail](docs/images/manual-testing/09-login-fail.png) |
| 13 | Auth | Register duplicate email | Error; no duplicate user | Pass |  | [10-register-duplicate](docs/images/manual-testing/10-register-duplicate.png) |
| 14 | Reviews | While logged out, open book detail | No POST review without login | Pass |  | [11-reviews-guest](docs/images/manual-testing/11-reviews-guest.png) |
| 15 | Reviews | Post a review (logged in) | Review appears on page | Pass |  | [12-review-created](docs/images/manual-testing/12-review-created.png) |
| 16 | Reviews | Edit **your** review | Updated text/rating shown | Pass |  | [13-review-edit](docs/images/manual-testing/13-review-edit.png) |
| 17 | Reviews | Delete **your** review | Review removed | Pass |  | [14-review-delete](docs/images/manual-testing/14-review-delete.png) |
| 18 | Reviews | Attempt to delete another user’s review (second account) | Blocked with message | Pass |  | [15-review-owner-block](docs/images/manual-testing/15-review-owner-block.png) |
| 19 | Cart | Add book to cart | Line appears with correct title/qty | Pass |  | [16-cart-add](docs/images/manual-testing/16-cart-add.png) |
| 20 | Cart | Change quantity / remove line | Totals and rows update | Pass |  | [17-cart-update-remove](docs/images/manual-testing/17-cart-update-remove.png)<br>[17b-cart-remove-confirm](docs/images/manual-testing/17b-cart-remove-confirm.png)<br>[17c-cart-updated](docs/images/manual-testing/17c-cart-updated.png) |
| 21 | Cart | Checkout with empty cart | Error flash; redirect to cart | Pass |  | [18-checkout-empty](docs/images/manual-testing/18-checkout-empty.png) |
| 22 | Orders | Checkout with items | Order on Orders page; cart empty | Pass |  | [19-checkout-success](docs/images/manual-testing/19-checkout-success.png)<br>[19b-orders-page](docs/images/manual-testing/19b-orders-page.png) |
| 23 | Admin | Open `/admin/analytics` as normal user | 403 Forbidden page | Pass |  |  |
| 24 | Admin | Same as admin user | Dashboard metrics load | Pass |  | [21-analytics-admin](docs/images/manual-testing/21-analytics-admin.png) |
| 25 | Admin | Add a new book via Analytics → Add book | Book created and visible in catalogue | Pass |  | [22-admin-add-book](docs/images/manual-testing/22-admin-add-book.png)<br>[23-admin-book-added](docs/images/manual-testing/23-admin-book-added.png) |
| 26 | Orders | Large order test (multiple items and quantities) | Cart subtotal matches checkout total; order summary lists all items | Pass |  | [27-large-order-cart](docs/images/manual-testing/27-large-order-cart.png)<br>[28-large-order-checkout](docs/images/manual-testing/28-large-order-checkout.png)<br>[29-large-order-checkout-total](docs/images/manual-testing/29-large-order-checkout-total.png) |
| 27 | Orders | Log out during checkout, then log back in | Redirects to login and returns to checkout (via `next=`); checkout can continue | Pass |  | [30-checkout-logout-login-continue](docs/images/manual-testing/30-checkout-logout-login-continue.png) |
| 28 | Auth | When logged in, check the navigation bar | Login/Register are hidden; authenticated links are shown instead (Cart/Orders/Logout) | Pass |  | [31-nav-logged-in-hides-login-register](docs/images/manual-testing/31-nav-logged-in-hides-login-register.png) |
| 29 | Reviews | Attempt to post a review while logged out | Redirects to login; after login the user can return and submit the review | Pass |  |  |
| 30 | Cart | Attempt “Add to cart” while logged out | Redirects to login; after login the user can add the book to cart | Pass |  |  |
| 31 | Admin | Add book: enter an invalid price (non-numeric or 0/negative) | Blocked with validation errors (“Price must be a number (e.g. 12.99).” / “Price must be greater than 0.”) | Pass |  |  |
| 32 | Cart | Update cart quantity using letters | Browser blocks non-numeric input (“Enter a number”) so quantity validation happens before submit | Pass |  | [35-cart-quantity-non-numeric](docs/images/manual-testing/35-cart-quantity-non-numeric.png) |

#### 404 page (assessor note + evidence)

- **Where to find it:** click **Sitemap** in the footer (route: **`/sitemap`**). This route is intentionally not implemented so the custom 404 page is shown.

![Custom 404 page](docs/images/validation/404-page.png)

Where something failed during manual runs, I kept **screenshots** or a short log and noted the fix in the bug table or devlog.

#### Validation and edge-case checks (input correctness)

These checks focus on places where user input can be correct/incorrect and where logic could break if validation was missing. Most validation is **server-side** (Flask routes) and is shown to the user via **flash messages**.

- **Register (`/register`)**
  - **Valid**: new email + matching passwords → account created and logged in.
  - **Invalid**:
    - duplicate email → blocked with a message (see manual test **#10**).
    - password confirmation mismatch → blocked with an error flash.

- **Login (`/login`)**
  - **Valid**: correct email/password → logged in and redirected.
  - **Invalid**: wrong password → stays on login with error flash (manual test **#9**).

- **Reviews (create/edit/delete)**
  - **Create review**:
    - blocked when logged out (redirect to login; manual test **#11**).
    - rating must be **1–5** and body must not be empty (server-side checks).
  - **Edit/delete**:
    - only the review owner can edit/delete (server-side ownership guard; manual tests **#13–#15**).

- **Cart**
  - **Quantity rules**: quantity < 1 is treated as remove (keeps totals consistent).
  - **Auth guard**: cart routes require login (tested in automated suite).

- **Checkout**
  - **Empty cart**: checkout is blocked with a flash + redirect back to cart (manual test **#18**).
  - **Valid**: creates an order + order items and clears the cart (manual test **#19**).

- **Admin-only routes**
  - Non-admins receive **403** on analytics and admin pages (manual test **#20**, automated tests).
  - Admin “Add book” checks:
    - required fields (title/author/price) must be present.
    - price must be numeric and > 0.
    - optional cover filename must exist under `static/img/covers/`.
    - duplicate (title + author) is blocked.

### Automated testing

For this project, I used **pytest** to write automated tests. The tests are located in the `tests/` directory and include:

- **`conftest.py`** — Sets `DATABASE_URL=sqlite:///:memory:` **before** the application module loads (so `create_app()` does not require PostgreSQL during `pytest`), resets the schema for each test, and provides shared fixtures (including a **`sample_book`** row inserted for detail/cart tests).
- **`test_public_pages.py`** — Checks the home page, contact page, books list, book detail, **404** for an unknown id, and that **static CSS** is served.
- **`test_auth.py`** — Exercises registration and login **GET** pages, the full **register → logout → login** flow, **password mismatch** on register, and **wrong password** on login.
- **`test_books_reviews.py`** — Verifies **search** (`?q=`), that **creating a review requires login**, and that a logged-in user can **post** a review. **Edit** and **delete** for reviews are covered in **manual** testing above only (not automated in the current suite).
- **`test_cart_orders_admin.py`** — Ensures the **cart** requires authentication, that items can be **added** to the cart, that **checkout with an empty cart** is handled, and that **admin analytics** requires login, returns **403** for a normal user, and **200** for an admin.

I was able to create these tests by following online tutorials and resources about testing Flask applications with pytest. Some helpful sources I used include:

- [Test a Flask App with pytest – Real Python](https://realpython.com/test-flask-apps/)
- [pytest documentation](https://docs.pytest.org/)
- [Testing Flask Applications – Flask documentation](https://flask.palletsprojects.com/en/stable/testing/)
- [pytest-flask documentation](https://pytest-flask.readthedocs.io/) — I did not use this plugin; the suite uses the stock Flask test client from `pytest` fixtures.

These resources helped me understand how to set up test environments, use an **in-memory database** for fast automated runs, and write **assertions** on HTTP status codes and HTML responses for different parts of the Flask app.

Below is a compact **feature → test** map showing what each automated test covers.

#### Feature → test mapping (simple)

| Feature | Test file | Test name | What it checks |
|--------|-----------|-----------|----------------|
| Home page loads | `test_public_pages.py` | `test_home_ok` | `GET /` returns 200 and expected text |
| Contact page loads | `test_public_pages.py` | `test_contact_ok` | `GET /contact` returns 200 |
| Books list loads | `test_public_pages.py` | `test_books_list_empty_ok` | `GET /books` returns 200 |
| Search works | `test_books_reviews.py` | `test_books_search_param_ok` | `?q=` returns matching book |
| Book detail loads | `test_public_pages.py` | `test_book_detail_ok` | `GET /books/<id>` shows title/author |
| Missing book returns 404 | `test_public_pages.py` | `test_book_detail_404` | Unknown id returns 404 |
| CSS is served | `test_public_pages.py` | `test_static_css_served` | `GET /static/css/styles.css` returns 200 |
| Register page loads | `test_auth.py` | `test_register_get_ok` | `GET /register` returns 200 |
| Login page loads | `test_auth.py` | `test_login_get_ok` | `GET /login` returns 200 |
| Register → logout → login | `test_auth.py` | `test_register_login_flow` | Full auth flow works |
| Register mismatch blocked | `test_auth.py` | `test_register_password_mismatch` | Mismatch redirects (validation path) |
| Wrong password blocked | `test_auth.py` | `test_login_bad_password` | Wrong password redirects to login |
| Review requires login | `test_books_reviews.py` | `test_create_review_requires_login` | Guest POST review redirects to login |
| Review can be created | `test_books_reviews.py` | `test_create_review_ok` | Logged-in user can post a review |
| Cart requires login | `test_cart_orders_admin.py` | `test_cart_requires_login` | Guest `GET /cart` redirects |
| Add to cart works | `test_cart_orders_admin.py` | `test_add_to_cart_ok` | Logged-in user can add a book |
| Empty cart checkout blocked | `test_cart_orders_admin.py` | `test_checkout_empty_cart_redirects` | Empty checkout handled safely |
| Admin analytics requires login | `test_cart_orders_admin.py` | `test_admin_analytics_requires_login` | Guest redirects to login |
| Admin analytics forbidden | `test_cart_orders_admin.py` | `test_admin_analytics_forbidden_for_normal_user` | Non-admin gets 403 |
| Admin analytics works | `test_cart_orders_admin.py` | `test_admin_analytics_ok_for_admin` | Admin gets 200 |

#### Limits (what automated tests do not cover)

- Payments are not integrated (checkout is “store the order”, not card processing).
- There is no email sending to test.
- UI layout changes are only checked where tests assert on key HTML text.

#### Running pytest locally (terminal evidence)

Because `pytest` is installed inside the project’s virtual environment, I activated the venv first and then ran the suite in verbose mode:

```bash
source .venv/bin/activate
pytest -v
```

Output from my local run:

```text
mohammedhussain@Mohammeds-MacBook-Air bookly-final % source .venv/bin/activate
pytest -v
===================== test session starts =====================
platform darwin -- Python 3.13.3, pytest-9.0.3, pluggy-1.6.0 -- /Users/mohammedhussain/Desktop/bookly-final/.venv/bin/python3.13
cachedir: .pytest_cache
rootdir: /Users/mohammedhussain/Desktop/bookly-final
configfile: pytest.ini
testpaths: tests
collected 23 items                                            

tests/test_auth.py::test_register_get_ok PASSED         [  4%]
tests/test_auth.py::test_login_get_ok PASSED            [  8%]
tests/test_auth.py::test_register_login_flow PASSED     [ 13%]
tests/test_auth.py::test_register_password_mismatch PASSED [ 17%]
tests/test_auth.py::test_login_bad_password PASSED      [ 21%]
tests/test_books_reviews.py::test_books_search_param_ok PASSED [ 26%]
tests/test_books_reviews.py::test_create_review_requires_login PASSED [ 30%]
tests/test_books_reviews.py::test_create_review_ok PASSED [ 34%]
tests/test_cart_orders_admin.py::test_cart_requires_login PASSED [ 39%]
tests/test_cart_orders_admin.py::test_add_to_cart_ok PASSED [ 43%]
tests/test_cart_orders_admin.py::test_checkout_empty_cart_redirects PASSED [ 47%]
tests/test_cart_orders_admin.py::test_admin_analytics_requires_login PASSED [ 52%]
tests/test_cart_orders_admin.py::test_admin_analytics_forbidden_for_normal_user PASSED [ 56%]
tests/test_cart_orders_admin.py::test_admin_analytics_ok_for_admin PASSED [ 60%]
tests/test_cart_orders_admin.py::test_admin_add_book_requires_login PASSED [ 65%]
tests/test_cart_orders_admin.py::test_admin_add_book_forbidden_for_normal_user PASSED [ 69%]
tests/test_cart_orders_admin.py::test_admin_add_book_ok_for_admin PASSED [ 73%]
tests/test_public_pages.py::test_home_ok PASSED         [ 78%]
tests/test_public_pages.py::test_contact_ok PASSED      [ 82%]
tests/test_public_pages.py::test_books_list_empty_ok PASSED [ 86%]
tests/test_public_pages.py::test_book_detail_404 PASSED [ 91%]
tests/test_public_pages.py::test_book_detail_ok PASSED  [ 95%]
tests/test_public_pages.py::test_static_css_served PASSED [100%]

====================== warnings summary =======================
tests/test_auth.py: 3 warnings
tests/test_books_reviews.py: 3 warnings
tests/test_cart_orders_admin.py: 16 warnings
  /Users/mohammedhussain/Desktop/bookly-final/app.py:48: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
    return User.query.get(uid)

tests/test_books_reviews.py::test_create_review_ok
tests/test_books_reviews.py::test_create_review_ok
tests/test_cart_orders_admin.py::test_add_to_cart_ok
tests/test_cart_orders_admin.py::test_admin_add_book_ok_for_admin
tests/test_public_pages.py::test_book_detail_404
tests/test_public_pages.py::test_book_detail_ok
  /Users/mohammedhussain/Desktop/bookly-final/.venv/lib/python3.13/site-packages/flask_sqlalchemy/query.py:30: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
    rv = self.get(ident)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============== 23 passed, 28 warnings in 2.12s ===============
(.venv) mohammedhussain@Mohammeds-MacBook-Air bookly-final %
```


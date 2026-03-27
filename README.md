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


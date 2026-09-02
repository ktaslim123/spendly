# Spec: Registration

## Overview
Implements user account creation for Spendly. The `/register` route currently
only renders a static template with no form handling — this step wires it up
to accept a POST submission, validate input, hash the password, insert a new
row into the `users` table, and start a logged-in session so the user lands
in the app immediately after signing up. This is the second step on the
roadmap and the first to introduce session-based authentication, which later
steps (login, logout, profile, expenses) will all depend on.

## Depends on
Step 01 — Database Setup (`users` table, `get_db()`, `init_db()`, `seed_db()`,
password hashing via `werkzeug.security`).

## Routes
- `GET /register` — renders the registration form — public
- `POST /register` — validates input, creates the user, starts session, redirects — public

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`,
`password_hash`, `created_at`) already supports registration as defined in
`database/db.py`. The `email` column's `UNIQUE NOT NULL` constraint is relied
upon to reject duplicate signups.

## Templates
- **Create:** none — `templates/register.html` already exists with the
  required form (`name`, `email`, `password` fields, POST to `/register`,
  and an `{% if error %}` block for validation messages).
- **Modify:** none required. If validation needs to redisplay previously
  entered `name`/`email` on error, `register.html` may optionally be updated
  to repopulate those two fields via `value="{{ name or '' }}"` etc.

## Files to change
- `app.py` — replace the stub `register()` view with GET/POST handling:
  validate form input, check for existing email, hash password, insert user,
  set session, redirect to a logged-in page (`/profile`, per roadmap Step 4 —
  until that exists, redirect to `/` as a placeholder is acceptable).

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` via `database/db.py` only.
- Parameterised queries only — never string-format values into SQL.
- Passwords hashed with `werkzeug.security.generate_password_hash`; never
  store or log plaintext passwords.
- Use CSS variables — never hardcode hex values (only relevant if
  `register.html` or `style.css` are touched).
- All templates extend `base.html`.
- Validate on the server even though HTML5 `required`/`type=email` exist
  client-side — never trust client-side validation alone.
- Re-render `register.html` with an `error` message on validation failure
  (missing fields, invalid email format, password under 8 characters,
  duplicate email) — do not redirect on error.
- On success, use Flask's `session` (server-side, signed cookie) to store the
  new user's `id`; do not implement a custom auth token scheme.
- Use the existing fixed `CATEGORIES` list only if touched incidentally —
  not relevant to this step but must not be broken.

## Definition of done
- [ ] Visiting `/register` in a browser renders the existing form with no errors.
- [ ] Submitting the form with a new name/email/password (8+ characters)
      creates a row in `users` with a hashed (not plaintext) password.
- [ ] After successful registration, the session contains the new user's id
      and the browser is redirected away from `/register`.
- [ ] Submitting with an email that already exists (e.g. `demo@spendly.com`)
      re-renders `register.html` with an error message and does not insert
      a duplicate row.
- [ ] Submitting with a missing name, missing email, invalid email format,
      or password under 8 characters re-renders the form with an
      appropriate error message and does not insert a row.
- [ ] Restarting the app (`python app.py`) after registering a user does not
      lose or duplicate that user's row.

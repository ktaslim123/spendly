# Spec: Login and Logout

## Overview
Implements session-based sign-in and sign-out for existing users. `/login`
currently only renders a static template with no form handling, and
`/logout` is an unimplemented placeholder route. This step wires both up:
`/login` validates credentials against the `users` table and starts a
session (mirroring the session pattern introduced in registration),
`/logout` clears that session. It also updates the shared nav in
`base.html` to reflect whether a visitor is signed in, since that is
currently hardcoded to always show "Sign in" / "Get started". This is the
third step on the roadmap and the second to touch session-based auth,
which the profile and expense-management steps will depend on.

## Depends on
- Step 01 — Database Setup (`users` table, `get_db()`).
- Step 02 — Registration (`session["user_id"]` convention, password hashing
  via `werkzeug.security`, established validation/re-render pattern in
  `app.py`'s `register()` view).

## Routes
- `GET /login` — renders the login form — public
- `POST /login` — validates credentials, starts session, redirects — public
- `GET /logout` — clears the session, redirects to landing page — logged-in
  (safe to call while logged out too; simply no-ops the session clear)

## Database changes
No database changes. Login reads existing `users` rows
(`email`, `password_hash`) via `database/db.py`; logout touches only the
Flask session, not the database.

## Templates
- **Create:** none — `templates/login.html` already exists with the
  required form (`email`, `password` fields, POST to `/login`, and an
  `{% if error %}` block for validation messages).
- **Modify:**
  - `templates/login.html` — repopulate the `email` field on validation
    error (`value="{{ email or '' }}"`), matching the pattern used in
    `register.html`.
  - `templates/base.html` — nav currently always renders "Sign in" /
    "Get started" links. Update to conditionally show "Sign in" /
    "Get started" when logged out, or a "Log out" link when
    `session.get("user_id")` is set. No profile link yet (profile page is
    Step 04 and not in scope here).

## Files to change
- `app.py`:
  - Replace the stub `login()` view with GET/POST handling: validate
    credentials, verify password with `werkzeug.security.check_password_hash`,
    set session, redirect on success; re-render with an error on failure.
  - Replace the stub `logout()` view: clear `session["user_id"]` (e.g.
    `session.pop("user_id", None)`) and redirect to the landing page.
- `templates/login.html` — repopulate `email` on error.
- `templates/base.html` — conditional nav based on session state.

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already
available (same package as `generate_password_hash`, used in Step 02).

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` via `database/db.py` only.
- Parameterised queries only — never string-format values into SQL.
- Passwords verified with `werkzeug.security.check_password_hash`; never
  compare plaintext passwords, never log passwords.
- Use CSS variables — never hardcode hex values.
- All templates extend `base.html`.
- Validate on the server even though HTML5 `required`/`type=email` exist
  client-side — never trust client-side validation alone.
- On failed login (unknown email, or wrong password), show a single
  generic error message (e.g. "Invalid email or password.") — do not
  reveal whether the email exists, to avoid user enumeration.
- Re-render `login.html` with the error on failure — do not redirect on
  error.
- On successful login, redirect to `/` (landing page), consistent with the
  registration flow's placeholder redirect target, since `/profile` (Step
  04) does not exist yet.
- `/logout` must work even if no session exists (no error, just redirect).

## Definition of done
- [ ] Visiting `/login` in a browser renders the existing form with no errors.
- [ ] Submitting the seeded demo credentials (`demo@spendly.com` /
      `demo123`) logs in successfully, sets the session, and redirects
      away from `/login`.
- [ ] Submitting a correct email with the wrong password re-renders
      `login.html` with a generic "Invalid email or password." error and
      does not set a session.
- [ ] Submitting an email that doesn't exist re-renders `login.html` with
      the same generic error message (not a different one) and does not
      set a session.
- [ ] Submitting with a missing email or missing password re-renders the
      form with an appropriate error and does not set a session.
- [ ] After logging in, the nav in `base.html` shows a "Log out" link
      instead of "Sign in" / "Get started".
- [ ] Visiting `/logout` while logged in clears the session and redirects
      to `/`; the nav reverts to showing "Sign in" / "Get started".
- [ ] Visiting `/logout` while already logged out does not error and
      redirects to `/`.

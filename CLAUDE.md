# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Spendly — a Flask + SQLite expense tracker, built incrementally as a learning project using Spec-Driven Development (SDD). See `docs/claude-code-learning-notes.md` for the workflow this project follows.

## Commands

- Activate venv: `source venv/Scripts/activate` (Git Bash) or `.\venv\Scripts\Activate.ps1` (PowerShell) — Windows venv uses `Scripts/`, not `bin/`. Must be re-activated per new terminal session.
- Install deps: `pip install -r requirements.txt`
- Run the app: `python app.py` (serves on `http://127.0.0.1:5001`, debug mode on)
- Run tests: `pytest` (test framework is installed via `pytest`/`pytest-flask` in `requirements.txt`; no test files exist yet)

There is no build step or linter configured.

## Architecture

**Spec-Driven Development workflow**: every feature starts as a spec document under `.claude/specs/NN-feature-name.md` (schema, functions, constraints, acceptance criteria) *before* any code is written. Work happens on a `feature/*` branch, uses Plan Mode to produce an implementation plan reviewed against the spec, then executes and validates against the spec's "Definition of Done" before merging via PR into `master` (the default branch — note GitHub's default is `main`, so pushes/PRs must target `master` explicitly).

**Database layer** (`database/db.py`): raw `sqlite3`, no ORM. Three functions define the entire data-access pattern:
- `get_db()` — opens a connection to `expense_tracker.db` (project root, gitignored) with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON` set explicitly on every connection (SQLite does not enable FK enforcement by default).
- `init_db()` — creates the `users` and `expenses` tables with `CREATE TABLE IF NOT EXISTS`; safe to call on every app startup.
- `seed_db()` — inserts one demo user + 8 sample expenses, guarded by checking for existing rows first so reruns never duplicate data.

Both `init_db()` and `seed_db()` are called inside `app.app_context()` at the top of `app.py`, so the schema and demo data are guaranteed to exist before any route runs.

Rules to preserve when extending this layer (from `.claude/specs/01-database-setup.md`):
- Parameterized queries only — never string-format values into SQL.
- `amount` is stored as `REAL`, not `INTEGER`.
- Dates are stored as `TEXT` in `YYYY-MM-DD` format.
- Passwords are hashed via `werkzeug.security.generate_password_hash` — never store plaintext.
- Expense categories are a fixed list (see `CATEGORIES` in `database/db.py`): Food, Transport, Bills, Health, Entertainment, Shopping, Other.

**App structure** (`app.py`): single-file Flask app, no blueprints. Routes fall into two groups:
- Implemented pages that render templates: `/`, `/register`, `/login`, `/terms`, `/privacy`.
- Placeholder routes returning plain strings, marked "coming in Step N" — these are intentionally unimplemented stubs for future SDD steps (`/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`). Don't "fix" these without a corresponding spec.

**Templates** (`templates/`): Jinja2 inheritance from `base.html`, which defines the shared nav/footer and `{% block title/head/content/scripts %}` blocks. All page templates extend it. Static assets live in `static/css/style.css` and `static/js/main.js`, referenced via `url_for('static', ...)`.

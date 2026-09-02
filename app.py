from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name:
        return render_template("register.html", error="Full name is required.",
                                name=name, email=email)
    if not email:
        return render_template("register.html", error="Email address is required.",
                                name=name, email=email)
    if "@" not in email or "." not in email.split("@")[-1]:
        return render_template("register.html", error="Enter a valid email address.",
                                name=name, email=email)
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.",
                                name=name, email=email)

    conn = get_db()
    existing = conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return render_template("register.html", error="An account with this email already exists.",
                                name=name, email=email)

    password_hash = generate_password_hash(password)
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    session["user_id"] = user_id
    return redirect(url_for("landing"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email:
        return render_template("login.html", error="Email address is required.",
                                email=email)
    if not password:
        return render_template("login.html", error="Password is required.",
                                email=email)

    conn = get_db()
    user = conn.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.",
                                email=email)

    session["user_id"] = user["id"]
    return redirect(url_for("landing"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)

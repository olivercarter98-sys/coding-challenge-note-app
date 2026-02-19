import re
from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, insert_entry, get_all_entries, delete_entry, update_entry

app = Flask(__name__)
# In production this should be set via an environment variable e.g. os.environ.get('SECRET_KEY')
app.secret_key = "nota-secret-key-change-in-production"

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_form(name: str, email: str, notes: str) -> list[str]:
    errors = []
    if not name:
        errors.append("Name is required.")
    elif len(name) > 100:
        errors.append("Name must be 100 characters or fewer.")
    if not email:
        errors.append("Email is required.")
    elif not EMAIL_RE.match(email):
        errors.append("Please enter a valid email address.")
    if not notes:
        errors.append("Notes are required.")
    elif len(notes) > 1000:
        errors.append("Notes must be 1000 characters or fewer.")
    return errors


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name  = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        notes = request.form.get("notes", "").strip()

        errors = validate_form(name, email, notes)
        if errors:
            for err in errors:
                flash(err, "error")
            return render_template("index.html", entries=get_all_entries(),
                                   form={"name": name, "email": email, "notes": notes})

        insert_entry(name, email, notes)
        flash("Entry saved successfully.", "success")
        return redirect(url_for("index"))

    return render_template("index.html", entries=get_all_entries(), form={})


@app.route("/update/<int:entry_id>", methods=["POST"])
def update(entry_id: int):
    name  = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    notes = request.form.get("notes", "").strip()

    errors = validate_form(name, email, notes)
    if errors:
        for err in errors:
            flash(err, "error")
    elif update_entry(entry_id, name, email, notes):
        flash("Entry updated successfully.", "success")
    else:
        flash("Entry not found.", "error")
    return redirect(url_for("index"))


@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete(entry_id: int):
    if delete_entry(entry_id):
        flash("Entry deleted.", "success")
    else:
        flash("Entry not found.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
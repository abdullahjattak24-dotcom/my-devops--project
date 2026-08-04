from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "devopsproject"

# =========================
# Create Database
# =========================
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# Home
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# About
# =========================
@app.route("/about")
def about():
    return render_template("about.html")

# =========================
# Contact
# =========================
@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO contacts(name,email,message) VALUES (?,?,?)",
            (name, email, message)
        )

        conn.commit()
        conn.close()

        flash("✅ Your message has been sent successfully!")

        return redirect(url_for("contact"))

    return render_template("contact.html")

# =========================
# Show Messages
# =========================
@app.route("/messages")
def messages():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts")
    messages = cursor.fetchall()

    conn.close()

    return render_template("messages.html", messages=messages)

# =========================
# Delete Message
# =========================
@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM contacts WHERE id=?", (id,))

    conn.commit()
    conn.close()

    flash("🗑️ Message Deleted Successfully!")

    return redirect(url_for("messages"))

# =========================
# Run App
# =========================
if __name__ == "__main__":
    app.run(debug=True)
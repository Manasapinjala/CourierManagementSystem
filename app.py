from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import random
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "secret123"


# ---------------- DATABASE INITIALIZATION ----------------

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Couriers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS couriers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tracking_id TEXT,
    sender TEXT,
    receiver TEXT,
    source TEXT,
    destination TEXT,
    status TEXT
    )
    """)

    # Complaints table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    tracking_id TEXT,
    complaint TEXT
    )
    """)

    # Feedback table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    message TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- HOME PAGE ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- ADMIN LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect("/admin")

    return render_template("login.html")


# ---------------- ADMIN LOGOUT ----------------

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


# ---------------- ADMIN DASHBOARD ----------------

@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM couriers")
    couriers = cursor.fetchall()

    # Statistics
    cursor.execute("SELECT COUNT(*) FROM couriers")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM couriers WHERE status='Delivered'")
    delivered = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM couriers WHERE status='In Transit'")
    transit = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM couriers WHERE status='Order Placed'")
    pending = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        couriers=couriers,
        total=total,
        delivered=delivered,
        transit=transit,
        pending=pending
    )


# ---------------- ADD COURIER ----------------

@app.route("/add", methods=["POST"])
def add():

    sender = request.form["sender"]
    receiver = request.form["receiver"]
    source = request.form["source"]
    destination = request.form["destination"]
    status = request.form["status"]

    tracking_id = "TRK" + str(random.randint(100000, 999999))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO couriers (tracking_id,sender,receiver,source,destination,status) VALUES (?,?,?,?,?,?)",
        (tracking_id, sender, receiver, source, destination, status)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")


# ---------------- UPDATE STATUS ----------------

@app.route("/update/<tracking_id>", methods=["POST"])
def update(tracking_id):

    status = request.form["status"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE couriers SET status=? WHERE tracking_id=?",
        (status, tracking_id)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")


# ---------------- DELETE COURIER ----------------

@app.route("/delete/<tracking_id>")
def delete(tracking_id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM couriers WHERE tracking_id=?",
        (tracking_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")


# ---------------- CUSTOMER DASHBOARD ----------------

@app.route("/customer")
def customer():
    return render_template("customer.html")


# ---------------- TRACK COURIER ----------------

@app.route("/track", methods=["GET", "POST"])
def track():

    courier = None

    if request.method == "POST":

        tracking_id = request.form["tracking_id"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM couriers WHERE tracking_id=?",
            (tracking_id,)
        )

        courier = cursor.fetchone()
        conn.close()

    return render_template("track.html", courier=courier)


# ---------------- CUSTOMER SERVICE ----------------

@app.route("/service")
def service():
    return render_template("service.html")


# ---------------- SUBMIT COMPLAINT ----------------

@app.route("/complaint", methods=["POST"])
def complaint():

    name = request.form["name"]
    tracking_id = request.form["tracking_id"]
    complaint = request.form["complaint"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO complaints(name,tracking_id,complaint) VALUES (?,?,?)",
        (name, tracking_id, complaint)
    )

    conn.commit()
    conn.close()

    return redirect("/service")


# ---------------- SUBMIT FEEDBACK ----------------

@app.route("/feedback", methods=["POST"])
def feedback():

    name = request.form["name"]
    message = request.form["message"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO feedback(name,message) VALUES (?,?)",
        (name, message)
    )

    conn.commit()
    conn.close()

    return redirect("/service")


# ---------------- DOWNLOAD RECEIPT ----------------

@app.route("/receipt/<tracking_id>")
def receipt(tracking_id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM couriers WHERE tracking_id=?",
        (tracking_id,)
    )

    data = cursor.fetchone()
    conn.close()

    filename = "receipt.pdf"

    c = canvas.Canvas(filename)

    c.drawString(100, 800, "Courier Receipt")
    c.drawString(100, 760, "Tracking ID: " + data[1])
    c.drawString(100, 740, "Sender: " + data[2])
    c.drawString(100, 720, "Receiver: " + data[3])
    c.drawString(100, 700, "Source: " + data[4])
    c.drawString(100, 680, "Destination: " + data[5])
    c.drawString(100, 660, "Status: " + data[6])

    c.save()

    return send_file(filename, as_attachment=True)
# ---------------- VIEW COMPLAINTS ----------------

@app.route("/view_complaints")
def view_complaints():

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()

    conn.close()

    return render_template("complaints.html", complaints=complaints)


# ---------------- VIEW FEEDBACK ----------------

@app.route("/view_feedback")
def view_feedback():

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM feedback")
    feedback = cursor.fetchall()

    conn.close()

    return render_template("feedback.html", feedback=feedback)


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)
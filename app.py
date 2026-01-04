from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key_here"

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root111",
    database="repo_management"
)
cursor = db.cursor(dictionary=True)

# HOME
@app.route("/")
def home():
    return render_template("index.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password!", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        try:
            cursor.execute(
                "INSERT INTO users (full_name, username, email, password) VALUES (%s, %s, %s, %s)",
                (full_name, username, email, hashed_password)
            )
            db.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for("login"))
        except mysql.connector.IntegrityError:
            flash("Username or email already exists!", "error")
            return redirect(url_for("register"))

    return render_template("register.html")

# FEATURES
@app.route("/features")
def features():
    return render_template("features.html")

# DEMO
@app.route("/demo")
def demo():
    return render_template("demo.html")

# HELP
@app.route("/help")
def help():
    return render_template("help.html")

# PRIVACY
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name")
        category = request.form.get("category")
        experience = request.form.get("experience")
        message = request.form.get("message")

        try:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO feedback (name, category, experience, message) VALUES (%s, %s, %s, %s)",
                (name, category, experience, message)
            )
            db.commit()
            cursor.close()

            flash("Thank you for your feedback!", "success")
        except Exception as e:
            db.rollback()
            flash("Something went wrong. Please try again.", "error")
            print(e)

        return redirect(url_for("feedback"))

    return render_template("feedback.html")
   
if __name__ == "__main__":
    app.run(debug=True)

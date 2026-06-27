from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey"

conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT)
""")
conn.commit()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=generate_password_hash(request.form["password"])
        try:
            cur.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))
            conn.commit()
            return redirect("/")
        except:
            return "Username already exists"
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    username=request.form["username"]
    password=request.form["password"]

    cur.execute("SELECT * FROM users WHERE username=?",(username,))
    user=cur.fetchone()

    if user and check_password_hash(user[2],password):
        session["user"]=username
        return redirect("/dashboard")

    return "Invalid Login"

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html",user=session["user"])
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
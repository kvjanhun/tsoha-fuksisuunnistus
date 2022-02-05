from app import app
import users
from flask import redirect, render_template, request, session

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Juu ei.")
        return redirect("/")        


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")
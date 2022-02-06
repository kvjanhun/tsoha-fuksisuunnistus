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

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 3:
            return render_template("error.html", message="Liian lyhyt nimi")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat ovat erit")
        if password1 == "":
            return render_template("error.html", message="Salasana on pakollinen")

        if not users.register(username, password1):
            return render_template("error.html", message="Nyt ei onnistunut, koetapa uuestaan.")  
        return redirect("/")

@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/groups")
def groups():
    return render_template("groups.html")
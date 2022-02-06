from email import message
from app import app
import users
from flask import redirect, render_template, request, session

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
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

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 2:
            return render_template("error.html", message="Liian lyhyt nimi.")
        if len(username) > 30:
            return render_template("error.html", message="Liian pitkä nimi.")
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat ovat erit.")
        if password1 == "":
            return render_template("error.html", message="Kyl sul salasana pitää olla.")

        if not users.register(username, password1):
            return render_template("error.html", message="Nyt ei onnistunut, koetapa uuestaan.")  
        return redirect("/")

@app.route("/groups",methods=["GET"])
def groups():
    return render_template("groups.html")

@app.route("/own",methods=["GET"])
def user():
    if session.get("user_id"):
        return render_template("checkpoint.html", user_info=users.user_info(),
     checkpoint_info=users.checkpoint_info())
    else:
        return redirect("/login")

@app.route("/send",methods=["POST"])
def send():
    names = request.form["names"]
    phone = request.form["phone"]
    checkpoint = request.form["checkpoint"]
    location = request.form["location"]
    if not users.id_exists():
        if users.create_info(names, phone, checkpoint, location):
            return render_template("checkpoint.html", message="Tiedot päivitetty!")
        else:
            return render_template("error.html", message="Virhe tallennettaessa tietoja.")
    else:
        #TODO: UPDATE
        return redirect("/")
from flask import redirect, render_template, request, session
from app import app
import users

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
            return render_template("error.html", message="Kirjautuminen epäonnistui.")
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
    theme = request.form["theme"]
    location = request.form["location"]
    if not users.uid_exists():
        if users.create_info(names, phone, theme, location):
            return render_template("checkpoint.html", message="Tiedot päivitetty!")
        else:
            return render_template("error.html", message="Virhe tallennettaessa tietoja.")
    else:
        if users.update_info(names, phone, theme, location):
            return render_template("checkpoint.html", message="Tiedot päivitetty!")
        else:
            return render_template("error.html", message="Tietojen päivittäminen epäonnistui.")

@app.route("/checkpoint_overview", methods=["GET"])
def checkpoints():
    if session.get("user_id"):
        checkpoints=users.get_checkpoints()
        return render_template("checkpoint_overview.html", checkpoints=checkpoints)
    else:
        return redirect("/login")

@app.route("/checkpoint", methods=["GET"])
def checkpoint():
    if session.get("user_id"):
        checkpoint=users.get_single_checkpoint(request.args.get("view_checkpoint"))
        return render_template("view_single_checkpoint.html", 
                                checkpoint=checkpoint, uids=users.get_valid_uids_with_names())
    else:
        return redirect("/login")

@app.route("/testi")
def testi():
    return render_template("error.html", message=users.get_single_checkpoint(1))

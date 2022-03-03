from flask import redirect, render_template, request, session, abort
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
        
        # admin_status selector for development and demonstration purposes
        #   needs to be removed from:
        #   -   parameters below
        #   -   users.register(as_a_param)
        #   -   register.html
        if request.form.getlist("admin_cb"):
            admin_status = True
        else:
            admin_status = False

        if not users.register(username, password1, admin_status):
            return render_template("error.html", message="Nyt ei onnistunut, koetapa uuestaan.")
        return redirect("/")

@app.route("/groups",methods=["GET"])
def groups():
    return render_template("groups.html")

@app.route("/edit_checkpoint",methods=["GET"])
def own():
    if session.get("user_id"):
        return render_template("edit_checkpoint.html", user_info=users.get_user_info())
    else:
        return redirect("/")

@app.route("/user",methods=["GET"])
def user_redirect():
    if users.is_user():
        uid = str(users.get_uid())
        return redirect("/user/"+uid)
    else:
        return redirect("/")

@app.route("/user/<int:uid>",methods=["GET"])
def user(uid):
    if users.is_user():
        if users.get_uid() == uid:
            return render_template("view_single_checkpoint.html", 
                                    checkpoint=users.get_single_checkpoint(uid),
                                    select=False)
    return redirect("/")

@app.route("/send_checkpoint",methods=["POST"])
def send_checkpoint():
    if session["token"] != request.form["token"]:
        abort(403)
    names = request.form["names"]
    phone = request.form["phone"]
    theme = request.form["theme"]
    location = request.form["location"]
    if not users.uid_exists():
        if users.create_info(names, phone, theme, location):
            return render_template("edit_checkpoint.html", message="Tiedot päivitetty!")
        else:
            return render_template("error.html", message="Virhe tallennettaessa tietoja.")
    else:
        if users.update_info(names, phone, theme, location):
            return render_template("edit_checkpoint.html", message="Tiedot päivitetty!")
        else:
            return render_template("error.html", message="Tietojen päivittäminen epäonnistui.")

@app.route("/checkpoint_overview", methods=["GET"])
def checkpoints():
    if session.get("user_id"):
        checkpoints=users.get_checkpoints()
        return render_template("checkpoint_overview.html", checkpoints=checkpoints)
    else:
        return redirect("/")

@app.route("/checkpoint", methods=["GET"])
def checkpoint():
    if session.get("user_id"):
        checkpoint=users.get_single_checkpoint(request.args.get("view_checkpoint"))
        return render_template("view_single_checkpoint.html",
                                checkpoint=checkpoint, 
                                uids=users.get_valid_uids_with_names(),
                                select=True)
    else:
        return redirect("/")

@app.route("/groups_overview",methods=["GET"])
def groups_overview():
    return render_template("groups.html")

@app.route("/admin")
def admin():
    if session.get("user_id"):
        return render_template("admin.html")
    else:
        return redirect("/")

@app.route("/testi")
def testi():
    return render_template("error.html", message=users.get_user_info())

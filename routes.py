from functools import reduce
import re
from tabnanny import check
from flask import redirect, render_template, request, session, abort
from app import app
import reviews
import teams
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
            return render_template("index.html", 
                                    message="Kirjautuminen epäonnistui, yritä uudelleen!")
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
        if users.username_exists(username):
            return render_template("register.html",
                                    message="Käyttäjätunnus on jo käytössä.",
                                    username=username)
        if len(username) < 2:
            return render_template("register.html",
                                    message="""Liian lyhyt nimi. Käyttäjätunnuksen
                                               pituus tulee olla 2-20 merkkiä.""",
                                               username=username)
        if len(username) > 20:
            return render_template("register.html",
                                    message="""Liian pitkä nimi. Käyttäjätunnuksen
                                    pituus tulee olla 2-20 merkkiä.""",
                                    username=username)
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("register.html",
                                    message="Salasanat eivät täsmää keskenään.",
                                    username=username, password1=password1,
                                    password2=password2)
        if password1 == "":
            return render_template("register.html", 
                                    message="Salasana ei voi olla tyhjä.")
        
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
            return render_template("register.html", 
                                    message="Rekisteröinti epäonnistui, yritä uudelleen.")
        return redirect("/")

@app.route("/teams",methods=["GET"])
def teams_route():
    return render_template("teams.html")

@app.route("/edit_checkpoint",methods=["GET"])
def edit_checkpoint():
    if users.is_user():
        return render_template("edit_checkpoint.html", user_info=users.get_user_info())
    else:
        return redirect("/")

@app.route("/edit_checkpoint/",methods=["GET"])
def redirect_checkpoint():
    return redirect("/checkpoint")

@app.route("/edit_checkpoint/<int:uid>",methods=["GET"])
def edit_other_checkpoint(uid):
    if users.is_user():
        return render_template("edit_checkpoint.html",
                                user_info=users.get_others_info(uid),
                                admin_edit=True, uid=uid)
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
    if users.update_info(names, phone, theme, location):
        return render_template("edit_checkpoint.html",
                                message="Tiedot päivitetty!",
                                user_info=users.get_user_info())
    else:
        return render_template("edit_checkpoint.html",
                                message="Tietojen päivittäminen epäonnistui.",
                                user_info=users.get_user_info())

@app.route("/send_checkpoint/<int:uid>",methods=["POST"])
def send_other_checkpoint(uid):
    if session["token"] != request.form["token"]:
        abort(403)
    names = request.form["names"]
    phone = request.form["phone"]
    theme = request.form["theme"]
    location = request.form["location"]
    if users.update_others_info(uid, names, phone, theme, location):
        return render_template("edit_checkpoint.html",
                                message="Tiedot päivitetty!",
                                user_info=users.get_others_info(uid))
    else:
        return render_template("edit_checkpoint.html",
                                message="Tietojen päivittäminen epäonnistui.",
                                user_info=users.get_others_info(uid))

@app.route("/checkpoint_overview", methods=["GET"])
def checkpoints():
    if users.is_user() and users.is_admin():
        return render_template("checkpoint_overview.html", 
                                checkpoints=users.get_checkpoints())
    else:
        return redirect("/")

@app.route("/select_checkpoint", methods=["GET"])
def select_checkpoint():
    if users.is_user() and users.is_admin():
        checkpoint = users.get_single_checkpoint(request.args.get("view_checkpoint"))
        return render_template("view_single_checkpoint.html",
                                checkpoint=checkpoint, 
                                uids=users.get_valid_uids_with_names(),
                                select=True)
    else:
        return redirect("/")

@app.route("/teams_overview",methods=["GET","POST"])
def teams_overview():
    if request.method == "GET":
        if users.is_user() and users.is_admin():
            return render_template("teams.html", teamlist=teams.get_teams())
        else:
            return redirect("/")

    if request.method == "POST":
        if session["token"] != request.form["token"]:
            abort(403)
        name = request.form["name"]
        if len(name) > 0 and len(name) <= 50:
            if teams.create_team(name):
                return render_template("teams.html",
                                        teamlist=teams.get_teams(),
                                        message="Joukkue lisätty!")
            else:
                return render_template("teams.html",
                                        teamlist=teams.get_teams(),
                                        message="Jokin meni pieleen :))")
        else:
            return render_template("teams.html",
                                    teamlist=teams.get_teams(),
                                    message="""Nimen pituus tulee olla 1-50 merkkiä,
                                    mitään ei tallennettu. Yritä uudelleen.""")

@app.route("/remove_team/<int:team_id>",methods=["POST"])
def remove_team(team_id):
    if session["token"] != request.form["token"]:
            abort(403)
    if teams.rm_team(team_id):
        return render_template("teams.html",
                                teamlist=teams.get_teams(),
                                message="Joukkue poistettu!")
    else:
        return render_template("teams.html",
                                teamlist=teams.get_teams(),
                                message="Jokin meni pieleen :))")

@app.route("/review", methods=["GET"])
def review():
    if users.is_user():
        team_id = request.args.get("reviewable", 0)
        checkpoint_id = users.get_uid()
        if reviews.review_exists(team_id, checkpoint_id):
            review = reviews.get_single_review(team_id, checkpoint_id)[0]
        else:
            review = False
        return render_template("review.html",
                                teamlist=teams.get_teams(),
                                team=teams.get_single_team(team_id),
                                review=review)
    else:
        return redirect("/")

@app.route("/send_review/<int:team_id>", methods=["POST"])
def send_review(team_id):
    checkpoint_id = users.get_uid()
    points = request.form["points"]
    review = request.form["review_area"]
    if reviews.review_exists(team_id, checkpoint_id):
        if reviews.update_review(team_id, checkpoint_id, points, review):
            return redirect("/review")
        else:
            return redirect("/review")
    else:
        if reviews.create_review(team_id, checkpoint_id, points, review):
            return redirect("/review")
        else:
            return redirect("/review")

@app.route("/admin")
def admin():
    if users.is_user() and users.is_admin():
        return render_template("admin.html")
    else:
        return redirect("/")

@app.route("/testi")
def testi():
    return render_template("test.html", message=teams.get_teams())

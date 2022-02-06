import secrets
from db import db
from flask import redirect, session
from werkzeug.security import check_password_hash, generate_password_hash


def login(name, password):
    sql = "SELECT password, id, admin FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = name
    session["user_role"] = user[2]
    session["csrf_token"] = secrets.token_hex(32)
    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]

def register(name, password):
    hash_value = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (name, password, admin)
                 VALUES (:name, :password, FALSE)"""
        db.session.execute(sql, {"name":name, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(name, password)


def user_info():
    id = session["user_id"]
    sql = "SELECT names, phone FROM user_info WHERE user_id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()

def checkpoint_info():
    id = session["user_id"]
    sql = "SELECT theme, location FROM checkpoint WHERE user_id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()

def id_exists():
    id = session["user_id"]
    sql = "SELECT COUNT(*) FROM user_info WHERE user_id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()[0] > 0
    # Returns True if user_info table already contains session user id.

def create_info(names, phone, theme, location):
    try:
        id = session["user_id"]
        sql1 = """INSERT INTO user_info (user_id, names, phone)
                VALUES (:id, :names, :phone)"""
        sql2 = """INSERT INTO checkpoint (user_id, theme, location)
                VALUES (:id, :theme, :location)"""
        db.session.execute(sql1, {"id":id, "names":names, "phone":phone})
        db.session.execute(sql2, {"id":id, "theme":theme, "location":location})
        db.session.commit()
        return True
    except:
        return False
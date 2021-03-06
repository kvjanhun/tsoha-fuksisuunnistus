import secrets
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

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
    session["admin"] = user[2]
    session["token"] = secrets.token_hex(32)
    if not get_user_info():
        create_info("rastinvetäjien nimet", "puhelinnumero",
                    "rastinne nimi", "rastinne sijainti")
    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["admin"]
    del session["token"]

def register(name, password, admin_status):
    hash_value = generate_password_hash(password)
    try:
        if admin_status is True:
            sql = """INSERT INTO users (name, password, admin)
                     VALUES (:name, :password, TRUE)"""
            db.session.execute(sql, {"name":name, "password":hash_value})
            db.session.commit()
        else:
            sql = """INSERT INTO users (name, password, admin)
                     VALUES (:name, :password, FALSE)"""
            db.session.execute(sql, {"name":name, "password":hash_value})
            db.session.commit()
    except:
        return False
    return login(name, password)

def username_exists(username):
    sql = "SELECT COUNT(*) FROM users WHERE name LIKE :username"
    result = db.session.execute(sql, {"username":username}).fetchone()
    return result[0] > 0

def get_uid():
    return session.get("user_id", False)

def is_user():
    return get_uid() is not False

def is_admin():
    return session.get("admin", False)

def get_user_info():
    uid = session["user_id"]
    sql = """SELECT names, phone, theme, location
             FROM user_info u, checkpoints c
             WHERE u.user_id = c.user_id AND u.user_id=:id;"""
    return db.session.execute(sql, {"id":uid}).fetchone()

def get_others_info(uid):
    sql = """SELECT names, phone, theme, location
             FROM user_info u, checkpoints c
             WHERE u.user_id = c.user_id AND u.user_id=:id;"""
    return db.session.execute(sql, {"id":uid}).fetchone()

def uid_exists():
    """Returns True if user_info table already contains session user id."""
    uid = session["user_id"]
    sql = "SELECT COUNT(*) FROM user_info WHERE user_id=:id"
    return db.session.execute(sql, {"id":uid}).fetchone()[0] > 0

def checkpoint_count():
    sql = "SELECT COUNT(*) FROM checkpoints"
    return db.session.execute(sql).fetchone()[0]

def create_info(names, phone, theme, location):
    try:
        uid = session["user_id"]
        next_ordinal = checkpoint_count() + 1
        sql1 = """INSERT INTO user_info (user_id, names, phone)
                  VALUES (:id, :names, :phone)"""
        sql2 = """INSERT INTO checkpoints (user_id, theme, location, ordinal)
                  VALUES (:id, :theme, :location, :ordinal)"""
        db.session.execute(sql1, {"id":uid, "names":names, "phone":phone})
        db.session.execute(sql2, {"id":uid, "theme":theme, "location":location,
                                  "ordinal":next_ordinal})
        db.session.commit()
        return True
    except:
        return False

def update_info(names, phone, theme, location):
    try:
        uid = session["user_id"]
        sql1 = """UPDATE user_info SET names=:names, phone=:phone
                  WHERE user_id=:id"""
        sql2 = """UPDATE checkpoints SET theme=:theme, location=:location
                  WHERE user_id=:id"""
        db.session.execute(sql1, {"id":uid, "names":names, "phone":phone})
        db.session.execute(sql2, {"id":uid, "theme":theme, "location":location})
        db.session.commit()
        return True
    except:
        return False

def update_others_info(uid, names, phone, theme, location):
    try:
        sql1 = """UPDATE user_info SET names=:names, phone=:phone
                  WHERE user_id=:id"""
        sql2 = """UPDATE checkpoints SET theme=:theme, location=:location
                  WHERE user_id=:id"""
        db.session.execute(sql1, {"id":uid, "names":names, "phone":phone})
        db.session.execute(sql2, {"id":uid, "theme":theme, "location":location})
        db.session.commit()
        return True
    except:
        return False

def get_checkpoints():
    """Return all checkpoints' info as sqlalchemy.engine.result.RowProxy"""
    sql = """SELECT c.user_id, names, phone, theme, location, ordinal
             FROM checkpoints c JOIN user_info u 
             ON c.user_id=u.user_id"""
    return db.session.execute(sql).fetchall()

def get_single_checkpoint(uid):
    """Return single checkpoint info as sqlalchemy.engine.result.RowProxy"""
    sql = """SELECT c.user_id, names, phone, theme, location, ordinal
             FROM checkpoints c JOIN user_info u 
             ON c.user_id=u.user_id WHERE c.user_id=:uid"""
    return db.session.execute(sql, {"uid":uid}).fetchone()

def get_valid_uids():
    """Return a list of valid user_id integers"""
    sql = "SELECT user_id FROM user_info"
    query_result = db.session.execute(sql).fetchall()
    return [item[0] for item in query_result]

def get_valid_uids_with_names():
    """Return a list of valid user_ids and the corresponding names"""
    sql = "SELECT user_id, names FROM user_info"
    query_result = db.session.execute(sql).fetchall()
    return [(item[0], item[1]) for item in query_result]

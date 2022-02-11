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
    uid = session["user_id"]
    sql = "SELECT names, phone FROM user_info WHERE user_id=:id"
    return db.session.execute(sql, {"id":uid}).fetchone()

def checkpoint_info():
    uid = session["user_id"]
    sql = "SELECT theme, location FROM checkpoint WHERE user_id=:id"
    return db.session.execute(sql, {"id":uid}).fetchone()

def uid_exists():
    uid = session["user_id"]
    sql = "SELECT COUNT(*) FROM user_info WHERE user_id=:id"
    return db.session.execute(sql, {"id":uid}).fetchone()[0] > 0
    # Returns True if user_info table already contains session user id.

def create_info(names, phone, theme, location):
    try:
        uid = session["user_id"]
        sql1 = """INSERT INTO user_info (user_id, names, phone)
                VALUES (:id, :names, :phone)"""
        sql2 = """INSERT INTO checkpoint (user_id, theme, location)
                VALUES (:id, :theme, :location)"""
        db.session.execute(sql1, {"id":uid, "names":names, "phone":phone})
        db.session.execute(sql2, {"id":uid, "theme":theme, "location":location})
        db.session.commit()
        return True
    except:
        return False

def update_info(names, phone, theme, location):
    try:
        uid = session["user_id"]
        sql1 = """UPDATE user_info SET names=:names, phone=:phone
                WHERE user_id=:id"""
        sql2 = """UPDATE checkpoint SET theme=:theme, location=:location
                WHERE user_id=:id"""
        db.session.execute(sql1, {"id":uid, "names":names, "phone":phone})
        db.session.execute(sql2, {"id":uid, "theme":theme, "location":location})
        db.session.commit()
        return True
    except:
        return False

def get_checkpoints():
    """Return a dict containing all checkpoints info, key=user_id"""
    sql = "SELECT * FROM user_info u, checkpoint c WHERE u.user_id=c.user_id"
    query_result = db.session.execute(sql).fetchall()
    return {cp[1]:[cp[1], cp[2], cp[3], cp[6], cp[7]] for cp in query_result}

def get_single_checkpoint(uid):
    """Return single checkpoint info as sqlalchemy.engine.result.RowProxy"""
    sql = """SELECT * FROM user_info u, checkpoint c 
             WHERE u.user_id=:uid AND u.user_id=c.user_id"""
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

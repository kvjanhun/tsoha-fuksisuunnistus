from db import db

def create_team(name):
    try:
        sql = "INSERT INTO groups (name) VALUES (:name)"
        db.session.execute(sql, {"name":name})
        db.session.commit()
        return True
    except:
        return False

def get_teams():
    sql = "SELECT * FROM groups"
    return db.session.execute(sql).fetchall()

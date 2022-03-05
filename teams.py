from db import db

def create_team(name):
    try:
        next_id = get_team_count() + 1
        sql = "INSERT INTO groups (id, name) VALUES (:next_id, :name)"
        db.session.execute(sql, {"next_id":next_id, "name":name})
        db.session.commit()
        return True
    except:
        return False

def get_team_count():
    sql = "SELECT COUNT(*) FROM groups"
    return db.session.execute(sql).fetchone()[0]

def get_teams():
    sql = "SELECT * FROM groups"
    return db.session.execute(sql).fetchall()

def rm_team(team_id):
    try:
        sql = "DELETE FROM groups WHERE id=:team_id"
        db.session.execute(sql, {"team_id":team_id})
        db.session.commit()
        return True
    except:
        return False

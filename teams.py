from db import db

def create_team(name):
    try:
        next_id = get_min_free_id()
        sql = "INSERT INTO groups (id, name) VALUES (:next_id, :name)"
        db.session.execute(sql, {"next_id":next_id, "name":name})
        db.session.commit()
        return True
    except:
        return False

def get_team_ids():
    sql = "SELECT id FROM groups"
    return [x[0] for x in db.session.execute(sql).fetchall()]

def get_min_free_id():
    ids = get_team_ids()
    for i in range(1, max(ids)+1):
        if i not in ids:
            return i
    else:
        return max(ids)+1


def get_teams():
    sql = "SELECT * FROM groups ORDER BY id"
    return db.session.execute(sql).fetchall()

def rm_team(team_id):
    try:
        sql = "DELETE FROM groups WHERE id=:team_id"
        db.session.execute(sql, {"team_id":team_id})
        db.session.commit()
        return True
    except:
        return False

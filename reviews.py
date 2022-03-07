from db import db

def create_review(team_id, checkpoint_id, points, review):
    try:
        sql = """INSERT INTO reviews (team_id, checkpoint_id, points, review)
                 VALUES (:team_id, :checkpoint_id, :points, :review)"""
        db.session.execute(sql, {"team_id":team_id,
                                 "checkpoint_id":checkpoint_id,
                                 "points":points,
                                 "review":review})
        db.session.commit()
        return True
    except:
        return False

def update_review(team_id, checkpoint_id, points, review):
    try:
        sql = """UPDATE reviews SET points=:points, review=:review
                 WHERE team_id=:team_id AND checkpoint_id=:checkpoint_id"""
        db.session.execute(sql, {"team_id":team_id,
                                 "checkpoint_id":checkpoint_id,
                                 "points":points,
                                 "review":review})
        db.session.commit()
        return True
    except:
        return False

def get_reviews_by_checkpoint_id(checkpoint_id):
    sql = """SELECT team_id, checkpoint_id, points, review FROM reviews
             WHERE checkpoint_id=:checkpoint_id"""
    return db.session.execute(sql, {"checkpoint_id":checkpoint_id}).fetchall()

def get_reviews_by_team_id(team_id):
    sql = """SELECT team_id, checkpoint_id, points, review FROM reviews
             WHERE team_id=:team_id"""
    return db.session.execute(sql, {"team_id":team_id}).fetchall()

def get_single_review(team_id, checkpoint_id):
    sql = """SELECT team_id, checkpoint_id, points, review FROM reviews
             WHERE team_id=:team_id AND checkpoint_id=:checkpoint_id"""
    return db.session.execute(sql, {"team_id":team_id,
                                    "checkpoint_id":checkpoint_id}).fetchall()

def review_exists(team_id, checkpoint_id):
    return bool(get_single_review(team_id, checkpoint_id)) is not False

def sum_of_points_for_team(team_id):
    sql = "SELECT SUM(points) FROM reviews"
    return db.session.execute(sql, {"team_id":team_id}).fetchone()[0]

def individual_points_for_team(team_id):
    sql = "SELECT points FROM reviews WHERE team_id=:team_id"
    query_result = db.session.execute(sql, {"team_id":team_id}).fetchall()
    return (team_id, [x[0] for x in query_result])

def reviews_for_team(team_id):
    sql = "SELECT review FROM reviews WHERE team_id=:team_id"
    query_result = db.session.execute(sql, {"team_id":team_id}).fetchall()
    return (team_id, [x[0] for x in query_result])

def get_team_ids_reviewed():
    sql = "SELECT team_id FROM reviews"
    return {x[0] for x in db.session.execute(sql).fetchall()}

def get_top_teams():
    sql = """SELECT t.name, SUM(r.points), r.team_id
             FROM reviews r, teams t
             WHERE r.team_id=t.id
             GROUP BY r.team_id, t.name
             ORDER BY sum DESC"""
    query_result = db.session.execute(sql).fetchall()
    return query_result
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

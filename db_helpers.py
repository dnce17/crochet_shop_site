import sqlite3

def search_db(db_name, action):
    connect = sqlite3.connect(db_name)
    connect.row_factory = sqlite3.Row
    db = connect.cursor()
    db.execute(action)

    return [dict(item) for item in db.fetchall()]


def alter_db(db_name, action, tup=()):
    connect = sqlite3.connect(db_name)
    db = connect.cursor()
    db.execute(action, tup)

    # Needed to make changes permanent after page refresh
    connect.commit()
    connect.close()
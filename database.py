import sqlite3


conn = sqlite3.connect('users_list.db', check_same_thread=False)
sql = conn.cursor()


sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(id INTEGER PRIMARY KEY, name TEXT, number TEXT, lat TEXT, lng TEXT);')


def registration(user_id, user_name, user_number, user_location_lat, user_location_lng):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?);',
                (user_id, user_name, user_number,
                 user_location_lat, user_location_lng))
    conn.commit()


def check_user(user_id):
    if sql.execute('SELECT * FROM users WHERE id=?;', (user_id,)).fetchone():
        return True
    else:
        return False


def check_name(user_id):
    return sql.execute('SELECT * FROM users WHERE id=?;', (user_id,)).fetchone()



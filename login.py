import sqlite3


# ********Registered User Login********
def reg_login(cursor, email, password):
    cursor.execute('SELECT * FROM users WHERE users.email = ? AND users.pwd = ?', (email, password))
    if cursor.fetchall():
        return 1
    return 0


# ********Unregistered User Sing up********
def sign_up(cursor: object, email: object, name: object, pwd: object, city: object, gender: object) -> object:
    cursor.execute('INSERT INTO users (email, name, pwd, city, gender) values(?, ? ,? , ?, ?)',
                   (email, name, pwd, city, gender))


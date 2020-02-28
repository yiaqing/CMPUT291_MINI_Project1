import sqlite3


# ********Registered User Login********
def reg_login(cursor, email, password):
    cursor.execute('SELECT * FROM users WHERE users.email = ? AND users.pwd = ?;', (email, password))
    if cursor.fetchall():
        return email
    return 0


# ********Unregistered User Sing up********
def sign_up(conn, cursor, email, name, pwd, city, gender):
    cursor.execute('INSERT INTO users (email, name, pwd, city, gender) VALUES(?, ?, ?, ?, ?);',
                   (email, name, pwd, city, gender))
    conn.commit()
    return email

# ********Login interface********

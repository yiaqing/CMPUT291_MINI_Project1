import sqlite3

# ********Registered User Login********
def reg_login(cursor, email, password):
    cursor.execute('SELECT * FROM users WHERE users.email = ? AND users.pwd = ?', (email, password))
    if cursor.fetchall():
        return 1
    return 0

# ********Unregistered User Login********

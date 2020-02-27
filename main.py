import sqlite3
import sys

# ********Initialization********
def conn_db():
    conn = sqlite3.connect(sys.argv[1])
    cursor = conn.cursor()
    return cursor

# ********Registered User Login********
def reg_login(cursor, email, password):
    cursor.execute('SELECT * FROM users WHERE users.email = ? AND users.pwd = ?', (email, password))
    if cursor.fetchall():
        return 1
    return 0

# ********Unregistered User Login********



if __name__ == "__main__":
    cursor = conn_db()

    # ********Registered User Login Test********
    value1 = reg_login(cursor, 'dne@dne.com', 'password')
    print(value1)
    value2 = reg_login(cursor, 'ibev@gmail.com', 'password')
    print(value2)
    value3 = reg_login(cursor, 'rupertd@yahoo.ca', 'wrong')
    print(value3)
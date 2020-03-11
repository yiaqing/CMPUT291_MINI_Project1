import sqlite3


# ********Registered User Login********
def reg_login(cursor, email, password):
    email = email.lower()

    # Check if email exceeds the max length
    if len(email) > 20:
        print("email out of bounds")
        return 0

    # Check if password exceeds the max length
    if len(password) > 4:
        print("password out of bounds")
        return 0

    # Check if the user exists in the database and check if the password is correct
    # for the corresponding user
    cursor.execute('SELECT * FROM users WHERE users.email = ? AND users.pwd = ?;', (email, password))
    if cursor.fetchall():
        # return email if the user login up successfully
        return email
    return 0


# ********Unregistered User Sing up********
def sign_up(conn, cursor, email, name, pwd, city, gender):
    try:
        # Create a new account by insert email and password into table users
        cursor.execute('INSERT INTO users (email, name, pwd, city, gender) VALUES(?, ?, ?, ?, ?);',
                       (email, name, pwd, city, gender))
    except:
        # Duplicated user can not exist.
        print("user already exist.")
        return 0

    conn.commit()
    return email

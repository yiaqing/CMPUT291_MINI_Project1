import sqlite3


# ********Registered User Login********
def reg_login(cursor, email, password):
    email = email.lower()

    if len(email) > 20:
        print("email out of bounds")
        return 0

    if len(password) > 4:
        print("password out of bounds")
        return 0

    cursor.execute('SELECT * FROM users WHERE users.email = ? AND users.pwd = ?;', (email, password))
    if cursor.fetchall():
        return email
    return 0


# ********Unregistered User Sing up********
def sign_up(conn, cursor, email, name, pwd, city, gender):
    email = email.lower()
    name = name.title()
    city = city.capitalize()
    gender = gender.upper()

    if len(email) > 20:
        print("email out of bounds")
        return 0

    if len(name) > 16:
        print("name out of bounds")
        return 0

    if len(pwd) > 4:
        print("password out of bounds")
        return 0

    if len(city) > 15:
        print("city out of bounds")
        return 0

    if len(gender) > 1:
        print("gender out of bounds")
        return 0

    if (gender != "M") and (gender != "F"):
        print("gender out of bounds")
        return 0

    try:
        cursor.execute('INSERT INTO users (email, name, pwd, city, gender) VALUES(?, ?, ?, ?, ?);',
                       (email, name, pwd, city, gender))
    except:
        print("user already exist.")
        return 0

    conn.commit()
    return email

# ********Login interface********

import list_products
import injection_detection
import login
import getpass


# ********Login in********
def ui_user_login(cursor):
    print("********Login in********")
    print("Enter email: ", end='')
    email = input()
    print("Enter password: ", end='')
    password = input()

    # Check SQL Injection
    if (injection_detection.email_check(email) is not None) and (injection_detection.name_check(password) is not None):
        user = login.reg_login(cursor, email, password)
    else:
        print("Injection.")
        return 0

    # Login
    return user


# ********Sign up********
def ui_user_signup(conn, cursor):
    print("********Sign up********")
    print("Email: ", end='')
    email = input()
    print("Name: ", end='')
    name = input()
    print("Password: ", end='')
    pwd = getpass.getpass()
    print("City: ", end="")
    city = input()
    print("Gender(M/F): ", end="")
    gender = input()

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

    # Check SQL Injection
    if (injection_detection.email_check(email) is not None) and (injection_detection.pwd_check(pwd) is not None):
        user = login.sign_up(conn, cursor, email, name, pwd, city, gender)
    else:
        print("Injection.")
        return 0

    return user


# ********list_products********
def ui_list_products(cursor):
    results = list_products.list_products(cursor)
    print("|"+results[0][0].center(5)+"|", end="")
    print(results[0][1].center(30) + "|", end="")
    print(results[0][2].center(19) + "|", end="")
    print(results[0][3].center(16) + "|", end="")
    print(results[0][4].center(24) + "|")

    for i in range(1, len(results)):
        print("|" + str(results[i][0]).center(5) + "|", end="")
        print(str(results[i][1]).center(30) + "|", end="")
        print(str(results[i][2]).center(19) + "|", end="")
        print(str(results[i][3]).center(16) + "|", end="")
        print(str(results[i][4]).center(24) + "|")


# ********


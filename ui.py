import list_products
import injection_detection
import login
import search_sales
import getpass


# ********Login in********
def ui_user_login(cursor):
    print("********Login in********")
    print("Enter email: ", end='')
    email = input()
    email = email.lower()
    print("Enter password: ", end='')
    password = getpass.getpass()

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


# ********Menu********
def ui_login_menu(conn, cursor):
    while True:
        user = 0
        print("********Menu********")
        print("l: Login in")
        print("s: Sign up")
        selected = input()
        if selected == "l":
            user = ui_user_login(cursor)
        elif selected == "s":
            user = ui_user_signup(conn, cursor)
        else:
            print("No such selection.")

        if user != 0:
            print("\nLogin as " + user)
            return user
        else:
            print("Login in failed.")


# ********Write products review********
def ui_write_product_review(conn, cursor, product_list, current_user):
    print("********Write product review********")
    print("pid: ", end="")
    pid = input()
    print("rating: ", end="")
    rating = input()
    print("rtext: ", end="")
    rtext = input()
    pid = pid.upper()

    reviewer = current_user.lower()

    # Check if rating out of bounds
    if (float(rating) > 5) or (float(rating) < 0):
        print("rating out of bounds.")
        return 0

    # Check if pid out of bounds
    pids = []
    for i in range(1, len(product_list)):
        pids.append(product_list[i][0])
    if pid not in pids:
        print("pid out of bound")
        return 0

    # Check if rtext out of bounds
    if injection_detection.search(rtext):
        print("Injection.")
        return 0

    if len(rtext) > 20:
        print("rtext out of bounds")
        return 0

    list_products.write_preview(conn, cursor, pid, reviewer, rating, rtext)


# ********List all reviews of the product********
def ui_list_all_reviews(cursor, product_list):
    print("pid: ", end="")
    pid = input()

    pid = pid.upper()

    # Check if pid out of bounds
    pids = []
    for i in range(1, len(product_list)):
        pids.append(product_list[i][0])
    if pid not in pids:
        print("pid out of bound")
        return 0

    print("********List all reviews of the product********")
    results = list_products.list_reviews(cursor, pid)

    print("|" + results[0][0].center(5) + "|", end="")
    print(results[0][1].center(5) + "|", end="")
    print(results[0][2].center(19) + "|", end="")
    print(results[0][3].center(10) + "|", end="")
    print(results[0][4].center(24) + "|")

    for i in range(1, len(results)):
        print("|" + str(results[i][0]).center(5) + "|", end="")
        print(str(results[i][1]).center(5) + "|", end="")
        print(str(results[i][2]).center(19) + "|", end="")
        print(str(results[i][3]).center(10) + "|", end="")
        print(str(results[i][4]).center(24) + "|")


# ********List all active sales associated to the product********
def ui_list_all_active_sales(cursor, product_list):
    print("pid: ", end="")
    pid = input()

    pid = pid.upper()

    # Check if pid out of bounds
    pids = []
    for i in range(1, len(product_list)):
        pids.append(product_list[i][0])
    if pid not in pids:
        print("pid out of bound")
        return 0

    results = list_products.list_sales(cursor, pid)

    print("********List all active sales associated to the product********")
    print("|" + results[0][0].center(5) + "|", end="")
    print(results[0][1].center(20) + "|", end="")
    print(results[0][2].center(5) + "|", end="")
    print(results[0][3].center(10) + "|", end="")
    print(results[0][4].center(25) + "|", end="")
    print(results[0][5].center(16) + "|", end="")
    print(results[0][6].center(10) + "|")

    for i in range(1, len(results)):
        print("|" + str(results[i][0]).center(5) + "|", end="")
        print(str(results[i][1]).center(20) + "|", end="")
        print(str(results[i][2]).center(5) + "|", end="")
        print(str(results[i][3]).center(10) + "|", end="")
        print(str(results[i][4]).center(25) + "|", end="")
        print(str(results[i][5]).center(16) + "|", end="")
        print(str(results[i][6]).center(10) + "|")


# ********list_products********
def ui_list_products(conn, cursor, current_user):
    print("********List all products with some active sales associated to them********")
    results = list_products.list_products(cursor)
    print("|" + results[0][0].center(5) + "|", end="")
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

    while True:
        print("\n********Menu********")
        print("w: Write a product review by providing a review text and a rating (a number between 1 and 5 inclusive")
        print("r: List all reviews of the product.")
        print("s: List all active sales associated to the product")
        print("e: exit")

        selected = input()
        if (selected == "W") or (selected == "w"):
            ui_write_product_review(conn, cursor, results, current_user)

        elif (selected == "R") or (selected == "r"):
            ui_list_all_reviews(cursor, results)

        elif (selected == "S") or (selected == "s"):
            ui_list_all_active_sales(cursor, results)

        elif (selected == "E") or (selected == "e"):
            return 0

        else:
            print("No such option.")


# ********Search for sales********
def ui_search_keywords(conn, cursor):
    print("Keywords (split by space): ", end="")
    keywords_list = input()
    if injection_detection.search(keywords_list):
        print("SQL injection.")
        return 0

    keywords_list = keywords_list.split()

    print("********List all sales containing keywords********")
    results = search_sales.search_sales(conn, cursor, keywords_list)
    print("|" + results[0][0].center(5) + "|", end="")
    print(results[0][1].center(20) + "|", end="")
    print(results[0][2].center(10) + "|", end="")
    print(results[0][3].center(25) + "|", end="")
    print(results[0][4].center(10) + "|", end="")
    print(results[0][5].center(10) + "|")

    for i in range(1, len(results)):
        print("|" + str(results[i][0]).center(5) + "|", end="")
        print(str(results[i][1]).center(20) + "|", end="")
        print(str(results[i][2]).center(10) + "|", end="")
        print(str(results[i][3]).center(25) + "|", end="")
        print(str(results[i][4]).center(10) + "|", end="")
        print(str(results[i][5]).center(10) + "|")


# ********Search for sales********
def ui_search_for_sales(conn, cursor):
    while True:
        print("********Search for sales********")
        print("ss: Enter keywords to search sales")
        print("ee: Exit")
        selected = input()
        if (selected == "ss") or (selected == "SS"):
            ui_search_keywords(conn, cursor)

        elif (selected == "ee") or (selected == "EE"):
            print("Exit.")
            return 0


# ********Main loop********
def ui_main_loop(conn, cursor):
    current_user = ui_login_menu(conn, cursor)

    while True:
        print("********Menu********")
        print("lp: List products")
        print("ss: Search for sales")
        print("rr: Rachel")
        print("ps: Post a sale")
        print("su: Search for users")
        print("ee: Exit")

        selected = input()
        if (selected == "lp") or (selected == "LP"):
            ui_list_products(conn, cursor, current_user)

        elif (selected == "ss") or (selected == "SS"):
            ui_search_for_sales(conn, cursor)

        elif (selected == "rr") or (selected == "RR"):
            print("Not Finished Yet.")

        elif (selected == "ps") or (selected == "PS"):
            print("Not Finished Yet.")

        elif (selected == "su") or (selected == "SU"):
            print("Not Finished Yet.")

        elif (selected == "ee") or (selected == "EE"):
            print("Exit")
            return 0

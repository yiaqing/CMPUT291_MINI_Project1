import list_products
import injection_detection
import login
import search_sales
import post_sale
import search_user
import getpass
import re
import datetime
import follow_up
import sqlite3


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

    if len(rtext) > 100:
        print("rtext out of bounds")
        return 0

    list_products.write_preview(conn, cursor, pid, reviewer, rating, rtext)


# ********List all reviews of the product********
def ui_list_all_product_reviews(cursor, product_list):
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
def ui_list_all_active_sales(conn, cursor, product_list, current_user):
    print("pid: ", end="")
    pid = input()

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
    print(results[0][1].center(40) + "|", end="")
    print(results[0][2].center(19) + "|", end="")
    print(results[0][3].center(16) + "|")

    for i in range(1, len(results)):
        print("|" + str(results[i][0]).center(5) + "|", end="")
        print(str(results[i][1]).center(40) + "|", end="")
        print(str(results[i][2]).center(19) + "|", end="")
        print(str(results[i][3]).center(16) + "|")
    ui_follow_up(conn, cursor, results, current_user)


def ui_follow_up(conn, cursor, results, current_user):
    while True:
        print("\n********Menu********")
        print("sd: select a sale for detailed information")
        print("ee: EXIT")

        selected = input().lower()
        if selected == 'sd':
            selection = follow_up.display_all_sales(results)
            follow_up.display_information(cursor, selection)
            while True:
                print("\n********Menu********")
                print("pb: place a bid on the selected sale")
                print("ls: list all active sales of the seller")
                print("lr: list all reviews of the seller who made the selected sale")
                print("ee: EXIT")
                selected2 = input().lower()
                if selected2 == 'pb':
                    follow_up.place_bid(conn, cursor, selection, current_user)

                if selected2 == 'ls':
                    results = follow_up.list_sales(cursor)
                    print("********List all active sales associated to the product********")
                    print("|" + results[0][0].center(5) + "|", end="")
                    print(results[0][1].center(40) + "|", end="")
                    print(results[0][2].center(19) + "|", end="")
                    print(results[0][3].center(16) + "|")

                    for i in range(1, len(results)):
                        print("|" + str(results[i][0]).center(5) + "|", end="")
                        print(str(results[i][1]).center(40) + "|", end="")
                        print(str(results[i][2]).center(19) + "|", end="")
                        print(str(results[i][3]).center(16) + "|")

                if selected2 == 'lr':
                    results = follow_up.list_reviews(cursor, selection)
                    print("|" + results[0][0].center(30) + "|", end="")
                    print(results[0][1].center(25) + "|", end="")
                    print(results[0][2].center(10) + "|", end="")
                    print(results[0][3].center(40) + "|", end="")
                    print(results[0][4].center(10) + "|")
                    for i in range(1, len(results)):
                        print("|" + str(results[i][0]).center(30) + "|", end="")
                        print(str(results[i][1]).center(25) + "|", end="")
                        print(str(results[i][2]).center(10) + "|", end="")
                        print(str(results[i][3]).center(40) + "|", end="")
                        print(str(results[i][4]).center(10) + "|")

                if selected2 == 'ee':
                    exit()

        if selected == 'ee':
            exit()


# ********list products menu********
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
            ui_list_all_product_reviews(cursor, results)

        elif (selected == "S") or (selected == "s"):
            ui_list_all_active_sales(conn, cursor, results, current_user)

        elif (selected == "E") or (selected == "e"):
            return 0

        else:
            print("No such option.")


# ********Search for sales********
def ui_search_keywords(conn, cursor, current_user):
    print("Keywords (split by space): ", end="")
    keywords_list = input()
    keywords_list = keywords_list.lower()
    if injection_detection.search(keywords_list):
        print("SQL injection.")
        return 0

    keywords_list = keywords_list.split()

    print("********List all sales containing keywords********")
    results = search_sales.search_sales(conn, cursor, keywords_list)
    if len(results) == 1:
        print("NO SALES AVAILABLE FOR THE KEYWORDS ENTERED")
        print("TRY ANOTHER ONE")
        ui_search_keywords(conn, cursor, current_user)
    else:
        print("|" + results[0][0].center(5) + "|", end="")
        print(results[0][1].center(40) + "|", end="")
        print(results[0][2].center(19) + "|", end="")
        print(results[0][3].center(16) + "|")

        for i in range(1, len(results)):
            print("|" + str(results[i][0]).center(5) + "|", end="")
            print(str(results[i][1]).center(40) + "|", end="")
            print(str(results[i][2]).center(19) + "|", end="")
            print(str(results[i][3]).center(16) + "|")
        ui_follow_up(conn, cursor, results, current_user)


# ********Search for sales menu********
def ui_search_for_sales(conn, cursor, current_user):
    while True:
        print("********Search for sales********")
        print("ss: Enter keywords to search sales")
        print("ee: Exit")
        selected = input()
        if (selected == "ss") or (selected == "SS"):
            ui_search_keywords(conn, cursor, current_user)

        elif (selected == "ee") or (selected == "EE"):
            print("Exit.")
            return 0

        else:
            print("No such option.")


# ********Post a sale********
def ui_post_a_sale(conn, cursor, current_user):
    print("pid: ", end="")
    pid = input()
    if pid == "":
        pid = None

    print("rprice: ", end="")
    rprice = input()
    if rprice == "":
        rprice = None

    print("edate(yyyy-mm-dd): ", end="")
    edate = input()
    # Check if date is out of bounds
    if re.fullmatch(r"^((?!0000)[0-9]{4}-((0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-8])|(0[13-9]|1[0-2])-(29|30)|" \
                    r"(0[13578]|1[02])-31)|([0-9]{2}(0[48]|[2468][048]|[13579][26])|(0[48]|[2468][048]|[13579]" \
                    r"[26])00)-02-29)$", edate) is None:
        print("Date Not Formatted")
        return 0
    today = str(datetime.date.today())
    if today > edate:
        print("Date out of bounds")
        return 0

    print("descr: ", end="")
    descr = input()
    # Check if descr out of bounds
    if len(descr) > 25:
        print("descr out of bounds")
        return 0
    if injection_detection.search(descr):
        print("Injection.")
        return 0

    print("cond: ", end="")
    cond = input()
    # Check if cond out of bounds
    if len(cond) > 10:
        print("cond out of bounds")
        return 0
    if injection_detection.search(cond):
        print("Injection.")
        return 0

    post_sale.post_sale(conn, cursor, current_user, edate, descr, cond, pid, rprice)


# ********Post a sale menu********
def ui_post_sale(conn, cursor, current_user):
    while True:
        print("********Post a sale********")
        print("ps: Enter a product id, a sale end date and time, a sale description, a condition, and a reserved price")
        print("ee: Exit")
        selected = input()
        if (selected == "ps") or (selected == "PS"):
            ui_post_a_sale(conn, cursor, current_user)
        if (selected == "ee") or (selected == "EE"):
            return 0


# ********List all reviews of the user********
def ui_list_all_reviews(cursor, user_list):
    print("Email: ", end="")
    email = input()
    # Check if email out of bounds
    flag = 1
    for i in range(len(user_list)):
        if email == user_list[i][0]:
            flag = 0
    if flag:
        print("No such email.")
        return 0

    results = search_user.list_reviews(cursor, email)

    print("|" + results[0][0].center(30) + "|", end="")
    print(results[0][1].center(15) + "|", end="")
    print(results[0][2].center(10) + "|", end="")
    print(results[0][3].center(15) + "|", end="")
    print(results[0][4].center(10) + "|")

    for i in range(1, len(results)):
        print("|" + str(results[i][0]).center(30) + "|", end="")
        print(str(results[i][1]).center(15) + "|", end="")
        print(str(results[i][2]).center(10) + "|", end="")
        print(str(results[i][3]).center(15) + "|", end="")
        print(str(results[i][4]).center(10) + "|")


# ********List all active listings of the user********
def ui_list_all_active_users(cursor, user_list):
    print("Email: ", end="")
    email = input()
    # Check if email out of bounds
    flag = 1
    for i in range(len(user_list)):
        if email == user_list[i][0]:
            flag = 0
    if flag:
        print("No such email.")
        return 0

    results = search_user.list_active(cursor, email)

    print("|" + results[0][0].center(5) + "|", end="")
    print(results[0][1].center(20) + "|", end="")
    print(results[0][2].center(10) + "|", end="")
    print(results[0][3].center(15) + "|", end="")
    print(results[0][4].center(20) + "|", end="")
    print(results[0][5].center(10) + "|", end="")
    print(results[0][6].center(10) + "|")

    for i in range(1, len(results)):
        print("|" + str(results[i][0]).center(5) + "|", end="")
        print(str(results[i][1]).center(20) + "|", end="")
        print(str(results[i][2]).center(10) + "|", end="")
        print(str(results[i][3]).center(15) + "|", end="")
        print(str(results[i][4]).center(20) + "|", end="")
        print(str(results[i][5]).center(10) + "|", end="")
        print(str(results[i][6]).center(10) + "|")


# ********ui_write_review********
def ui_write_user_review(conn, cursor, user_list, reviewer):
    print("Reviewee email: ", end="")
    email = input()
    print("Rtext: ", end="")
    rtext = input()
    print("rating: ", end="")
    rating = input()
    rating = float(rating)

    # Check if email out of bounds
    flag = 1
    for i in range(len(user_list)):
        if email == user_list[i][0]:
            flag = 0
    if flag:
        print("No such email.")
        return 0

    # Check if rtext out of bounds
    if len(rtext) > 20:
        print("rtext out of bounds.")
    if injection_detection.search(rtext):
        print("Injection.")
        return 0

    # Check if rating out of bounds
    if (rating > 5) or (rating < 1):
        print("rating out of bounds.")

    # Check if the user review him or her self
    if reviewer == email:
        print("No self review.")
        return 0

    search_user.write_review(conn, cursor, reviewer, email, rtext, rating)


# ********Search for users menu********
def ui_search_for_users(conn, cursor, current_user):
    print("Enter keyword to search for users: ", end="")
    keyword = input()
    if injection_detection.search(keyword):
        print("SQL injection.")
        return 0

    print("********List all users containing keywords********")
    results = search_user.search_user(cursor, keyword)
    print("|" + results[0][0].center(20) + "|", end="")
    print(results[0][1].center(15) + "|", end="")
    print(results[0][2].center(10) + "|", end="")
    print(results[0][3].center(15) + "|", end="")
    print(results[0][4].center(6) + "|")

    for i in range(1, len(results)):
        print("|" + str(results[i][0]).center(20) + "|", end="")
        print(str(results[i][1]).center(15) + "|", end="")
        print(str(results[i][2]).center(10) + "|", end="")
        print(str(results[i][3]).center(15) + "|", end="")
        print(str(results[i][4]).center(6) + "|")

    while True:
        print("********Menu********")
        print("wr: Write a review")
        print("ll: List all active listing of the users")
        print("lr: List all reviews of the user")
        print("ee: Exit")

        selected = input()
        if (selected == "wr") or (selected == "WR"):
            ui_write_user_review(conn, cursor, results, current_user)
        elif (selected == "ll") or (selected == "LL"):
            ui_list_all_active_users(cursor, results)
        elif (selected == "lr") or (selected == "LR"):
            ui_list_all_reviews(cursor, results)
        elif (selected == "ee") or (selected == "EE"):
            return 0
        else:
            print("No such option.")


# ********Main loop********
def ui_main_loop(conn, cursor):
    # current_user = ui_login_menu(conn, cursor)
    current_user = 'ibev@gmail.com'
    while True:
        print("********Menu********")
        print("lp: List products")
        print("ss: Search for sales")
        print("ps: Post a sale")
        print("su: Search for users")
        print("ee: Exit")

        selected = input().lower()
        if selected == "lp":
            ui_list_products(conn, cursor, current_user)

        elif selected == "ss":
            ui_search_for_sales(conn, cursor, current_user)

        elif selected == "ps":
            ui_post_sale(conn, cursor, current_user)

        elif selected == "su":
            ui_search_for_users(conn, cursor, current_user)

        elif selected == "ee":
            print("Exit")
            return 0


# '''
# Test area
# if __name__ == "__main__":
#     conn = sqlite3.connect("db.db")
#     cursor = conn.cursor()
#     # ui_main_loop(conn, cursor)
#     # ui_search_for_users(conn, cursor, "rachel@gmail.com")
#     ui_search_for_sales(conn, cursor, "rachel@gmail.com")
# '''

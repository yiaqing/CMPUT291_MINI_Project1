import sqlite3
import sys
import login
import list_products
import search_sales
import post_sale
import search_user
import injection_detection

#zqq
# ********Initialization********
def conn_db():
    conn = sqlite3.connect(sys.argv[1])
    return conn


# ********Destruction********
def disconn_db(conn, cursor):
    cursor.close()
    conn.close()


# ********Main********
if __name__ == "__main__":
    conn = conn_db()
    cursor = conn.cursor()

    # ********Registered User Login Test********
    # value1 = login.reg_login(cursor, 'dne@dne.com', 'password')
    # print(value1)
    # value2 = login.reg_login(cursor, 'ibev@gmail.com', 'password')
    # print(value2)
    # value3 = login.reg_login(cursor, 'rupertd@yahoo.ca', 'wrong')
    # print(value3)

    # ********User Sign up Test********
    # login.sign_up(conn, cursor, 'abcdefghijklmn@t2.com', 't123', 't123', 'Edmonton', 'M')
    # login.sign_up(conn, cursor, 'abcdefghijklm@t2.com', 't123', 't123', 'Edmonton', 'A')
    # login.sign_up(conn, cursor, 'abcdefghijklm@t2.com', 't12344', 't12444443', 'Edmonton', 'F')

    # login.sign_up(conn, cursor, 'test1@test.test', 'racHel z', 'test', 'Montreal', 'F')

    # ********Listing Products Test********
    value = list_products.list_products(cursor)
    for i in range(0, len(value)):
        print(value[i])

    # ********Write product review test********
    # list_products.write_preview(conn, cursor, value, 'G11', 'ibev@gmail.com', '5', 'test')
    # list_products.write_preview(conn, cursor, value, 'G01', 'ibev@gmail.com', '5', 'testtesttesttesttesta')
    # list_products.write_preview(conn, cursor, value, 'G01', 'ibev@gmail.com', '-1', 'test')
    # list_products.write_preview(conn, cursor, value, 'G01', 'ibev@gmail.com', '6', 'test')

    # list_products.write_preview(conn, cursor, value, 'M01', 'ibev@gmail.com', '5', 'test')
    # list_products.write_preview(conn, cursor, value, 'G01', 'ibev@gmail.com', '5', 'test')

    # ********List reviews test********
    # list_products.list_reviews(cursor, value, 'g10000')
    # list_products.list_reviews(cursor, value, 'g11')
    # list_products.list_reviews(cursor, value, 'G01')
    # list_products.list_reviews(cursor, value, 'g01')
    # list_products.list_reviews(cursor, value, 'M01')

    # ********List all associative active sales test********
    print("-------------------------------------------------")
    associative_sales = list_products.list_sales(cursor, value, 'G01')
    if associative_sales:
        for i in range(0, len(associative_sales)):
            print(associative_sales[i])

    print("-------------------------------------------------")

    associative_sales = list_products.list_sales(cursor, value, 'M03')
    if associative_sales:
        for i in range(0, len(associative_sales)):
            print(associative_sales[i])

    print("-------------------------------------------------")

    associative_sales = list_products.list_sales(cursor, value, 'P01')
    if associative_sales:
        for i in range(0, len(associative_sales)):
            print(associative_sales[i])

    print("-------------------------------------------------")

    associative_sales = list_products.list_sales(cursor, value, 'M02')
    if associative_sales:
        for i in range(0, len(associative_sales)):
            print(associative_sales[i])

    print("-------------------------------------------------")

    associative_sales = list_products.list_sales(cursor, value, 'MMMMM')
    if associative_sales:
        for i in range(0, len(associative_sales)):
            print(associative_sales[i])

    print("-------------------------------------------------")

    value = search_sales.search_sales(conn, cursor, ['common', 'rachel'])
    for i in range(len(value)):
        print(value[i])

    print("-------------------------------------------------")

    post_sale.post_sale(conn, cursor, "ibev@gmail.com", "2020-03-31", "Test", "Test")

    print("-------------------------------------------------")

    print(search_user.search_user(cursor, 'edmonton'))

    print("-------------------------------------------------")

    search_user.write_review(conn, cursor, "abanner@ualberta.ca", "ibev@gmail.com", "bad", 1)

    print("-------------------------------------------------")

    value = search_user.list_active(cursor, "ibev@gmail.com")
    for i in range(len(value)):
        print(value[i])

    print("-------------------------------------------------")

    value = search_user.list_reviews(cursor, "ibev@gmail.com")
    for i in range(len(value)):
        print(value[i])

    print("-------------------------------------------------")

    injection_detection.search("*")

    print("-------------------------------------------------")

    # ********Disconnect Database********
    disconn_db(conn, cursor)

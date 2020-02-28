import sqlite3
import sys
import login
import list_products


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
    value1 = login.reg_login(cursor, 'dne@dne.com', 'password')
    print(value1)
    value2 = login.reg_login(cursor, 'ibev@gmail.com', 'password')
    print(value2)
    value3 = login.reg_login(cursor, 'rupertd@yahoo.ca', 'wrong')
    print(value3)

    # ********User Sign up Test********
    # login.sign_up(conn, cursor, 't3@t2.com', 't123', 't123', 'Edmonton', 'M')

    # ********Listing Products Test********
    value = list_products.list_products(cursor)
    for i in range(0, len(value)):
        print(value[i])

    # ********Write product review test********
    list_products.write_preview(conn, cursor, 'G11', 'ibev@gmail.com', '5', 'test')
    list_products.write_preview(conn, cursor, 'G01', 'ibev@gmail.com', '5', 'testtesttesttesttesta')
    list_products.write_preview(conn, cursor, 'G01', 'ibev@gmail.com', '-1', 'test')
    list_products.write_preview(conn, cursor, 'G01', 'ibev@gmail.com', '6', 'test')

    list_products.write_preview(conn, cursor, 'G01', 'ibev@gmail.com', '5', 'test')

    # ********Disconnect Database********
    disconn_db(conn, cursor)

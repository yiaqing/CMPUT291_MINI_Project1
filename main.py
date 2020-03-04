import sqlite3
import sys
import login
import list_products
import search_sales
import post_sale
import search_user
import injection_detection
import ui
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
    cursor.execute('''PRAGMA foreign_keys = ON;''')

    ui.ui_list_products(conn, cursor, "ibev@gmail.com")

    # ********Disconnect Database********
    disconn_db(conn, cursor)

import sqlite3
import sys
import ui


# zqq
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

    ui.ui_main_loop(conn, cursor)

    # ********Disconnect Database********
    disconn_db(conn, cursor)

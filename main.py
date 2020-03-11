import sqlite3
import sys
import ui


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
    try:
        conn = conn_db()
    except:
        print("Database connection error.")
        exit()

    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = ON;''')

    ui.ui_main_loop(conn, cursor)

    # ********Disconnect Database********
    disconn_db(conn, cursor)
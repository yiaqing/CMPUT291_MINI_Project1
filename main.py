import sqlite3
import sys
import login

# ********Initialization********
def conn_db():
    conn = sqlite3.connect(sys.argv[1])
    cursor = conn.cursor()
    return cursor


if __name__ == "__main__":
    cursor = conn_db()

    # ********Registered User Login Test********
    value1 = login.reg_login(cursor, 'dne@dne.com', 'password')
    print(value1)
    value2 = login.reg_login(cursor, 'ibev@gmail.com', 'password')
    print(value2)
    value3 = login.reg_login(cursor, 'rupertd@yahoo.ca', 'wrong')
    print(value3)
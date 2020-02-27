import sqlite3
import sys

# ********Initialization********
def conn_db():
    conn = sqlite3.connect(sys.argv[1])
    cursor = conn.cursor()
    return cursor

if __name__ == "__main__":
    cursor = conn_db()


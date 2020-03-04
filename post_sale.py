import sqlite3
import re


# Q4
# ********Post a sale********
def post_sale(conn, cursor, lister, edate, descr, cond, pid=None, rprice=None):
    cursor.execute('''SELECT MAX(sales.sid)
                      FROM sales;''')
    sid = cursor.fetchall()[0][0]
    sid_num = str(int(sid[1:]) + 1)
    sid_char = sid[0]
    sid = sid_char + sid_num

    # Check if pid out of bounds
    if pid is not None:
        cursor.execute('''SELECT *
                          FROM products
                          WHERE products.pid = ?;''', (pid, ))
        if not cursor.fetchall():
            print("pid out of bounds")
            return 0

    cursor.execute('''INSERT INTO sales (sid, lister, pid, edate, descr, cond, rprice)
                      VALUES (?, ?, ?, ?, ?, ?, ?);''', (sid, lister, pid, edate, descr, cond, rprice))
    conn.commit()


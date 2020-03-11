import sqlite3
import re


# Q4
# ********Post a sale********
def post_sale(conn, cursor, lister, edate, descr, cond, pid=None, rprice=None):
    # Get the next unique sales sid
    # by implementing MAX function
    cursor.execute('''SELECT MAX(sales.sid)
                      FROM sales;''')

    # Concatenate the first letter with the index
    sid = cursor.fetchall()[0][0]
    sid_num = str(int(sid[1:]) + 1)
    sid_char = sid[0]
    sid = sid_char + sid_num

    # Check if pid out of bounds
    if pid is not None:
        # If the certain products exists, get all the info regarding this product.
        cursor.execute('''SELECT *
                          FROM products
                          WHERE products.pid = ?;''', (pid, ))
        if not cursor.fetchall():
            # Check if the certain product exists.
            print("pid out of bounds")
            return 0

    # Insert the sales information to the sales table
    # pid and rprice could be NULL
    cursor.execute('''INSERT INTO sales (sid, lister, pid, edate, descr, cond, rprice)
                      VALUES (?, ?, ?, ?, ?, ?, ?);''', (sid, lister, pid, edate, descr, cond, rprice))
    conn.commit()


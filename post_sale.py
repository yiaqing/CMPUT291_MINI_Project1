import sqlite3
import re
import datetime


# Q4
# ********Post a sale********
def post_sale(conn, cursor, lister, edate, descr, cond, pid=None, rprice=None):
    cursor.execute('''SELECT MAX(sales.sid)
                      FROM sales;''')
    sid = cursor.fetchall()[0][0]
    sid_num = str(int(sid[1:]) + 1)
    sid_char = sid[0]
    sid = sid_char + sid_num

    # Check if date is out of bounds
    if re.match(r"^((?!0000)[0-9]{4}-((0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-8])|(0[13-9]|1[0-2])-(29|30)|" \
                r"(0[13578]|1[02])-31)|([0-9]{2}(0[48]|[2468][048]|[13579][26])|(0[48]|[2468][048]|[13579]" \
                r"[26])00)-02-29)$", edate) is None:
        print("Date Not Formatted")
        return 0
    today = str(datetime.date.today())
    if today > edate:
        print("Date out of bounds")
        return 0

    # Check if descr out of bounds
    if len(descr) > 25:
        print("descr out of bounds")
        return 0

    # Check if cond out of bounds
    if len(cond) > 10:
        print("cond out of bounds")
        return 0

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


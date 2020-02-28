import sqlite3


# ********List qualifying products information********
def list_products(cursor):
    cursor.execute('''SELECT products.pid, products.descr, COUNT(DISTINCT previews.rid) AS number_of_reviews, \
                      AVG(previews.rating) AS average_rating, COUNT(DISTINCT sales.sid) AS number_of_active_sales \
                      FROM (products LEFT OUTER JOIN sales ON products.pid = sales.pid) \
                      LEFT OUTER JOIN previews ON products.pid = previews.pid \
                      WHERE sales.edate > DATE('now') \
                      GROUP BY products.pid \
                      ORDER BY number_of_active_sales DESC;''')
    return cursor.fetchall()


# ********Write product review********
def write_preview(conn, cursor, pid, reviewer, rating, rtext):
    # Check if rating out of bounds
    if (float(rating) > 5) or (float(rating) < 0):
        print("rating out of bounds.")
        return 0

    # Check if pid out of bounds
    cursor.execute('''SELECT products.pid FROM products;''')
    pids = cursor.fetchall()
    flag = 0
    for i in range(len(pids)):
        if pids[i][0] == pid:
            flag = 1
    if not flag:
        print("pid out of bounds")
        return 0

    # Check if rtext out of bounds
    if len(rtext) > 20:
        print("rtext out of bounds")
        return 0

    # Get next unique rid
    cursor.execute('''SELECT MAX(rid) FROM previews;''')
    rid = cursor.fetchall()[0][0] + 1

    cursor.execute('''INSERT INTO previews (rid, pid, reviewer, rating, rtext, rdate) \
                      VALUES (?, ?, ?, ?, ?, DATE('now'));''', (rid, pid, reviewer, rating, rtext))
    conn.commit()


# ********List reviews of product********
def list_reviews(cursor, pid):
    # Check if pid out of bounds
    cursor.execute('''SELECT products.pid FROM products;''')
    pids = cursor.fetchall()
    flag = 0
    for i in range(len(pids)):
        if pids[i][0] == pid:
            flag = 1
    if not flag:
        print("pid out of bounds")
        return 0

    cursor.execute('''SELECT * FROM previews WHERE previews.pid = ?''', (pid, ))
    reviews = cursor.fetchall()
    for i in range(len(reviews)):
        print(reviews[i])

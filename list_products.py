import sqlite3


# Q1
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
def write_preview(conn, cursor, product_list, pid, reviewer, rating, rtext):
    pid = pid.upper()
    reviewer = reviewer.lower()

    # Check if rating out of bounds
    if (float(rating) > 5) or (float(rating) < 0):
        print("rating out of bounds.")
        return 0

    # Check if pid out of bounds
    pids = []
    for i in range(len(product_list)):
        pids.append(product_list[i][0])
    if pid not in pids:
        print("pid out of bound")
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
def list_reviews(cursor, product_list, pid):
    pid = pid.upper()

    # Check if pid out of bounds
    pids = []
    for i in range(len(product_list)):
        pids.append(product_list[i][0])
    if pid not in pids:
        print("pid out of bound")
        return 0

    cursor.execute('''SELECT * FROM previews WHERE previews.pid = ?;''', (pid, ))
    reviews = cursor.fetchall()
    for i in range(len(reviews)):
        print(reviews[i])


# *********List all associative active sales********
def list_sales(cursor, product_list, pid):
    pid = pid.upper()

    # Check if pid out of bounds
    pids = []
    for i in range(len(product_list)):
        pids.append(product_list[i][0])
    if pid not in pids:
        print("pid out of bound")
        return 0

    cursor.execute('''SELECT sales.sid AS sid, sales.lister AS lister, \
                      sales.pid AS pid, sales.edate AS edate, sales.descr AS descr, \
                      sales.cond AS cond, sales.rprice AS rprice \
                      FROM sales
                      WHERE sales.pid = ?
                      AND sales.edate > DATE('now')
                      ORDER BY sales.edate ASC;''', (pid, ))

    return cursor.fetchall()


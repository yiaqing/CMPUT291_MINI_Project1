import sqlite3


# Q1
# ********List qualifying products information********
def list_products(cursor):
    # Select the info from table products and sales
    # Join these two tables together on pid to gather the info
    # sales.edate must be in the future
    # the results is sorted by number of sales
    cursor.execute('''SELECT products.pid, products.descr, COUNT(DISTINCT previews.rid) AS number_of_reviews, \
                      ROUND(AVG(previews.rating), 2) AS average_rating, COUNT(DISTINCT sales.sid) AS number_of_active_sales \
                      FROM (products LEFT OUTER JOIN sales ON products.pid = sales.pid) \
                      LEFT OUTER JOIN previews ON products.pid = previews.pid \
                      WHERE sales.edate > DATE('now') \
                      GROUP BY products.pid \
                      ORDER BY number_of_active_sales DESC;''')
    column_title = [[]]
    for i in range(len(cursor.description)):
        column_title[0].append(cursor.description[i][0])

    results = []
    temp = cursor.fetchall()
    for i in range(len(temp)):
        results.append(list(temp[i]))

    results = column_title + results
    return results


# ********Write product review********
def write_preview(conn, cursor, pid, reviewer, rating, rtext):
    # Get next unique rid
    cursor.execute('''SELECT MAX(rid) FROM previews;''')
    rid = cursor.fetchall()[0][0] + 1

    # Insert the previews into table previews
    # rating and rtext from user input
    cursor.execute('''INSERT INTO previews (rid, pid, reviewer, rating, rtext, rdate) \
                      VALUES (?, ?, ?, ?, ?, DATE('now'));''', (rid, pid, reviewer, rating, rtext))
    conn.commit()


# ********List reviews of product********
def list_reviews(cursor, pid):
    # Select all product reviews from previews tables
    cursor.execute('''SELECT * FROM previews WHERE previews.pid = ?;''', (pid,))
    column_title = [[]]
    for i in range(len(cursor.description)):
        column_title[0].append(cursor.description[i][0])
    reviews = cursor.fetchall()
    results = []
    for i in range(len(reviews)):
        results.append(list(reviews[i]))

    results = column_title + results

    return results


# *********List all associative active sales********
def list_sales(cursor, pid):
    # Join table sales and bids on sid
    # select info sales.sid, sale.description, max bid amount.
    # If there is no bid, reserved price will be the min bid amount
    # CAST is implemented to convert time to remaining time
    cursor.execute('''SELECT    sales.sid, 
                                sales.descr, 
                                case WHEN  bids.amount is null
                                        then sales.rprice
                                    ELSE max(bids.amount)
                                END status,
                                CAST((strftime('%s', sales.edate) - strftime('%s', 'now')) / (60 * 60 * 24) AS TEXT) || ' days ' ||
                                CAST(((strftime('%s', sales.edate) - strftime('%s', 'now')) % (60 * 60 * 24)) / (60 * 60) AS TEXT) || ':' ||
                                CAST((((strftime('%s', sales.edate) - strftime('%s', 'now')) % (60 * 60 * 24)) % (60 * 60)) / 60 AS TEXT) AS time 
                        FROM sales LEFT OUTER JOIN bids ON sales.sid = bids.sid
                        WHERE sales.pid = ?
                        AND sales.edate > DATE('now')
                        GROUP BY sales.sid
                        ORDER BY sales.edate ASC;''',  (pid,))
    column_title = [[]]
    for i in range(len(cursor.description)):
        column_title[0].append(cursor.description[i][0])
    reviews = cursor.fetchall()
    results = []
    for i in range(len(reviews)):
        results.append(list(reviews[i]))
    results = column_title + results

    return results

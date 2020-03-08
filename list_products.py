import sqlite3


# Q1
# ********List qualifying products information********


def list_products(cursor):
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

    cursor.execute('''INSERT INTO previews (rid, pid, reviewer, rating, rtext, rdate) \
                      VALUES (?, ?, ?, ?, ?, DATE('now'));''', (rid, pid, reviewer, rating, rtext))
    conn.commit()


# ********List reviews of product********
def list_reviews(cursor, pid):
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
    # cursor.execute('''SELECT sales.sid AS sid, sales.lister AS lister, \
    #                   sales.pid AS pid, sales.edate AS edate, sales.descr AS descr, \
    #                   sales.cond AS cond, sales.rprice AS rprice \
    #                   FROM sales
    #                   WHERE sales.pid = ?
    #                   AND sales.edate > DATE('now')
    #                   ORDER BY sales.edate ASC;''', (pid,))
    cursor.execute('''SELECT    sales.sid, 
                                sales.descr, 
                                case bids.amount
                                    WHEN null 
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

'''
test
if __name__ == "__main__":
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    print("********List all products with some active sales associated to them********")
    results = list_sales(cursor, 'G01')
    print("|" + results[0][0].center(5) + "|", end="")
    print(results[0][1].center(30) + "|", end="")
    print(results[0][2].center(19) + "|", end="")
    print(results[0][3].center(16) + "|")

    for i in range(1, len(results)):
        print("|" + str(results[i][0]).center(5) + "|", end="")
        print(str(results[i][1]).center(30) + "|", end="")
        print(str(results[i][2]).center(19) + "|", end="")
        print(str(results[i][3]).center(16) + "|")
'''
import sqlite3


# ********Helper Function of search for sales*********
def helper(cursor, keywords):
    keywords = '%' + keywords + '%'
    cursor.execute('''SELECT *
                      FROM
                      (SELECT t1.sid, SUM(t1.cnt) AS keyword_count
                      FROM
                      (SELECT sales.sid, p.cnt
                      FROM
                      ((SELECT products.pid, COUNT(products.pid) AS cnt
                      FROM products
                      WHERE products.descr LIKE ?
                      GROUP BY products.pid) p LEFT OUTER JOIN sales ON p.pid = sales.pid)

                      UNION ALL

                      SELECT sales.sid, COUNT(sales.sid) AS cnt
                      FROM sales
                      WHERE sales.descr LIKE ?
                      GROUP BY sales.sid) t1
                      GROUP BY t1.sid) t2, sales
                      WHERE t2.sid = sales.sid
                      AND sales.edate > DATE('now');''', (keywords, keywords))

    return cursor.fetchall()

# ********Search for sales********
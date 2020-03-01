import sqlite3


# Q2
# ********Helper Function of search for sales*********
def helper(cursor, keyword):
    keyword = '%' + keyword + '%'
    cursor.execute('''SELECT t2.sid, t2.keyword_count, sales.lister, sales.pid, sales.edate, sales.descr, sales.cond, \
                      sales.rprice
                      FROM
                      (SELECT t1.sid AS sid, SUM(t1.cnt) AS keyword_count
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
                      AND sales.edate > DATE('now');''', (keyword, keyword))

    return cursor.fetchall()


# ********Search for sales********
def search_sales(conn, cursor, keywords_list):
    sales = []

    cursor.execute('''CREATE TEMPORARY TABLE ptemp(
                      sid char(20),
                      keyword_cnt int,
                      lister char(20),
                      pid char(20),
                      edate DATE,
                      descr char(25),
                      cond char(20),
                      rprice int);''')

    for i in range(len(keywords_list)):
        value = helper(cursor, keywords_list[i])
        for j in range(len(value)):
            sales.append(value[j])

    for i in range(len(sales)):
        cursor.execute('''INSERT INTO ptemp (sid, keyword_cnt, lister, pid, edate, descr, cond, rprice) \
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (sales[i][0], sales[i][1], sales[i][2], sales[i][3], \
                                                           sales[i][4], sales[i][5], sales[i][6], sales[i][7]))

    cursor.execute('''SELECT ptemp.sid, ptemp.lister, ptemp.edate, ptemp.descr, ptemp.cond, ptemp.rprice
                      FROM ptemp
                      GROUP BY ptemp.sid
                      ORDER BY SUM(ptemp.keyword_cnt) DESC;
                    ''')

    return cursor.fetchall()


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
                      WHERE products.descr LIKE ? COLLATE NOCASE
                      GROUP BY products.pid) p LEFT OUTER JOIN sales ON p.pid = sales.pid)

                      UNION ALL

                      SELECT sales.sid, COUNT(sales.sid) AS cnt
                      FROM sales
                      WHERE sales.descr LIKE ? COLLATE NOCASE
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
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?);''', [sales[i][0], sales[i][1], sales[i][2], sales[i][3], \
                                                                sales[i][4], sales[i][5], sales[i][6], sales[i][7],])

    # cursor.execute('''SELECT ptemp.sid, ptemp.lister, ptemp.edate, ptemp.descr, ptemp.cond, ptemp.rprice
    #                   FROM ptemp
    #                   GROUP BY ptemp.sid
    #                   ORDER BY SUM(ptemp.keyword_cnt) DESC;
    #                 ''')

    cursor.execute('''SELECT    ptemp.sid, ptemp.descr,
                                case bids.amount
                                    WHEN not null
                                        then max(bids.amount)
                                    ELSE ptemp.rprice
                                END status,
                                CAST((strftime('%s', ptemp.edate) - strftime('%s', 'now')) / (60 * 60 * 24) AS TEXT) || ' days ' ||
                                CAST(((strftime('%s', ptemp.edate) - strftime('%s', 'now')) % (60 * 60 * 24)) / (60 * 60) AS TEXT) || ':' ||
                                CAST((((strftime('%s', ptemp.edate) - strftime('%s', 'now')) % (60 * 60 * 24)) % (60 * 60)) / 60 AS TEXT) AS time
                        FROM ptemp LEFT OUTER JOIN bids ON ptemp.sid = bids.sid
                        GROUP BY ptemp.sid
                        ORDER BY SUM(ptemp.keyword_cnt) DESC;
                        ''')

    column_title = [[]]
    for i in range(len(cursor.description)):
        column_title[0].append(cursor.description[i][0])
    reviews = cursor.fetchall()
    results = []
    for i in range(len(reviews)):
        results.append(list(reviews[i]))
    results = column_title + results

    cursor.execute('''DROP TABLE ptemp;''')

    conn.commit()

    return results

# zqq
if __name__ == "__main__":
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    print("********List all sales containing keywords********")
    results = search_sales(conn, cursor, 'common')
    print("|" + results[0][0].center(5) + "|", end="")
    print(results[0][1].center(40) + "|", end="")
    print(results[0][2].center(19) + "|", end="")
    print(results[0][3].center(16) + "|")

    for i in range(1, len(results)):
        print("|" + str(results[i][0]).center(5) + "|", end="")
        print(str(results[i][1]).center(40) + "|", end="")
        print(str(results[i][2]).center(19) + "|", end="")
        print(str(results[i][3]).center(16) + "|")

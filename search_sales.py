import sqlite3


# Q2
# ********Helper Function of search for sales*********
def helper(cursor, keyword):
    # Concatenate keyword with % to implement LIKE
    keyword = '%' + keyword + '%'
    # First select sid and number of keywords appeared in sales
    # Then select sid and number of keywords appeared in products
    # Union these tables and select all the sales info regarding the
    # selected sales from the table derived from union result.
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
                      AND sales.edate > DATE('now', 'localtime');''', (keyword, keyword))
    return cursor.fetchall()


# ********Search for sales********
def search_sales(conn, cursor, keywords_list):
    sales = []

    # Create a temporary table
    # Then insert all the results derived from the function above
    # to give the statistics of the keywords appeared in each sale
    cursor.execute('''CREATE TEMPORARY TABLE ptemp(
                      sid char(20),
                      keyword_cnt int,
                      lister char(20),
                      pid char(20),
                      edate DATE,
                      descr char(25),
                      cond char(20),
                      rprice int);''')

    # Process the results from helper function
    # The results is converted to list
    for i in range(len(keywords_list)):
        value = helper(cursor, keywords_list[i])
        for j in range(len(value)):
            sales.append(value[j])

    # Insert data in to the temporary able from the results derived from union table
    # It gives the number of keywords appeared in the selected sales
    for i in range(len(sales)):
        cursor.execute('''INSERT INTO ptemp (sid, keyword_cnt, lister, pid, edate, descr, cond, rprice) \
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?);''', [sales[i][0], sales[i][1], sales[i][2], sales[i][3], \
                                                                sales[i][4], sales[i][5], sales[i][6], sales[i][7],])

    # Select sid and description and min bid if there is bid
    # using reversed price instead if there exists no bid
    # CAST function is implemented to convert the time to remaining time
    # the results are order by number of keywords in each sale
    cursor.execute('''SELECT    ptemp.sid, ptemp.descr, IFNULL(max(bids.amount), ptemp.rprice) AS max_bid,
                                CAST((strftime('%s', ptemp.edate) - strftime('%s', 'now')) / (60 * 60 * 24) AS TEXT) || ' days ' ||
                                CAST(((strftime('%s', ptemp.edate) - strftime('%s', 'now')) % (60 * 60 * 24)) / (60 * 60) AS TEXT) || ':' ||
                                CAST((((strftime('%s', ptemp.edate) - strftime('%s', 'now')) % (60 * 60 * 24)) % (60 * 60)) / 60 AS TEXT) AS time
                                FROM ptemp LEFT OUTER JOIN bids ON ptemp.sid = bids.sid
                                GROUP BY ptemp.sid
                                ORDER BY SUM(ptemp.keyword_cnt) DESC;
                   ''')

    # The results are processed to convert to list with column name
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

import sqlite3


# Q5
# ********Search for users********
def search_user(cursor, keyword):
    keyword = '%' + keyword + '%'
    cursor.execute('''SELECT *
                      FROM users
                      WHERE users.email LIKE ? COLLATE NOCASE
                      OR users.name LIKE ? COLLATE NOCASE 
                      OR users.city LIKE ? COLLATE NOCASE;''', (keyword, keyword, keyword))
    column_title = [[]]
    for i in range(len(cursor.description)):
        column_title[0].append(cursor.description[i][0])
    reviews = cursor.fetchall()
    results = []
    for i in range(len(reviews)):
        results.append(list(reviews[i]))
    results = column_title + results

    return results


# ********Write a review********
def write_review(conn, cursor, reviewer, reviewee, rtext, rating):
    try:
        cursor.execute('''INSERT INTO reviews (reviewer, reviewee, rating, rtext, rdate)
                          VALUES (?, ?, ?, ?, DATE('now'));''', (reviewer, reviewee, rating, rtext))
    except:
        print("Already reviewed")
        return 0

    conn.commit()


# ********List active sales********
def list_active(cursor, email):
    cursor.execute('''SELECT sales.sid, sales.lister, sales.pid, sales.edate, sales.descr, sales.cond, sales.rprice
                      FROM users LEFT OUTER JOIN sales ON users.email = sales.lister
                      WHERE users.email = ?
                      AND sales.edate > DATE('now')
                      ORDER by sales.edate;''', (email, ))

    column_title = [[]]
    for i in range(len(cursor.description)):
        column_title[0].append(cursor.description[i][0])
    reviews = cursor.fetchall()
    results = []
    for i in range(len(reviews)):
        results.append(list(reviews[i]))
    results = column_title + results

    return results


# ********List reviews********
def list_reviews(cursor, email):
    cursor.execute('''SELECT reviews.reviewer, reviews.reviewee, reviews.rating, reviews.rtext, reviews.rdate
                      FROM reviews
                      WHERE reviews.reviewee = ?;''', (email, ))

    column_title = [[]]
    for i in range(len(cursor.description)):
        column_title[0].append(cursor.description[i][0])
    reviews = cursor.fetchall()
    results = []
    for i in range(len(reviews)):
        results.append(list(reviews[i]))
    results = column_title + results

    return results

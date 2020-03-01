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
    return cursor.fetchall()


# ********Write a review********
def write_review(conn, cursor, reviewer, reviewee, rtext, rating):
    # Check if rtext out of bounds
    if len(rtext) > 20:
        print("rtext out of bounds.")

    # Check if rating out of bounds
    if (rating > 5) or (rating < 1):
        print("rating out of bounds.")

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
    return cursor.fetchall()


# ********List reviews********
def list_reviews(cursor, email):
    cursor.execute('''SELECT reviews.reviewer, reviews.reviewee, reviews.rating, reviews.rtext, reviews.rdate
                      FROM reviews
                      WHERE reviews.reviewee = ?;''', (email, ))
    return cursor.fetchall()

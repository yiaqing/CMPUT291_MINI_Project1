import sqlite3


# Q5
# ********Search for users********
def search_user(cursor, keyword):
    # Concatenate the strings to enable the use of LIKE function
    keyword = '%' + keyword + '%'
    # Select users containing the keywords
    # the keywords are set to be case insensitive
    cursor.execute('''SELECT *
                      FROM users
                      WHERE users.email LIKE ? COLLATE NOCASE
                      OR users.name LIKE ? COLLATE NOCASE 
                      OR users.city LIKE ? COLLATE NOCASE;''', (keyword, keyword, keyword))

    # Process the results to convert it to list
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
    # Set reviewer to case insensitive
    cursor.execute('''SELECT users.email
                      FROM users
                      WHERE users.email = ? COLLATE NOCASE''', (reviewer, ))
    reviewer = cursor.fetchall()[0][0]

    # Set reviewee to case insensitive
    cursor.execute('''SELECT users.email
                      FROM users
                      WHERE users.email = ? COLLATE NOCASE''', (reviewee, ))
    reviewee = cursor.fetchall()[0][0]

    try:
        # Insert the review to the user
        cursor.execute('''INSERT INTO reviews (reviewer, reviewee, rating, rtext, rdate)
                          VALUES (?, ?, ?, ?, DATE('now'));''', (reviewer, reviewee, rating, rtext))
    except:
        # Check if there is duplicated reviews
        # One user cannot review the same user twice
        print("Already reviewed")
        return 0

    conn.commit()


# ********List active sales********
def list_active(cursor, email):
    # Select the active sales and combined it with the lister
    # the sales must be active and is bounded by edate > now
    # users and sales are joined to gather the info
    cursor.execute('''SELECT sales.sid, sales.lister, sales.pid, sales.edate, sales.descr, sales.cond, sales.rprice
                      FROM users LEFT OUTER JOIN sales ON users.email = sales.lister
                      WHERE users.email = ? COLLATE NOCASE
                      AND sales.edate > DATE('now')
                      ORDER by sales.edate;''', (email, ))

    # Process the results to convert it to list
    # with column name
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
    # select all the reviews of a user
    # the user name is from user in put
    cursor.execute('''SELECT reviews.reviewer, reviews.reviewee, reviews.rating, reviews.rtext, reviews.rdate
                      FROM reviews
                      WHERE reviews.reviewee = ? COLLATE NOCASE;''', (email, ))

    # Process the results to convert it to list
    # with column name
    column_title = [[]]
    for i in range(len(cursor.description)):
        column_title[0].append(cursor.description[i][0])
    reviews = cursor.fetchall()
    results = []
    for i in range(len(reviews)):
        results.append(list(reviews[i]))
    results = column_title + results

    return results

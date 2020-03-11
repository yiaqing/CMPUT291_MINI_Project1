import sqlite3
from time import gmtime, strftime
import uuid


def display_all_sales(results):
    print("Select one sales followed for more detailed information")
    for i in range(len(results)):
        print("|" + str(results[i][0]).center(5) + "|")
    selection = input()
    return selection


def display_information(cursor, selection):
    print("selection:", selection)
    cursor.execute('''SELECT  sales.lister,
                            COUNT(reviews.reviewer) as number_of_ratings, ROUND(AVG(reviews.rating), 2) as average_rating,
                            sales.descr, sales.edate, sales.cond,
                            case WHEN bids.amount is null
                                    then sales.rprice
                                ELSE max(bids.amount)
                            END status
                    FROM    sales LEFT OUTER JOIN reviews ON sales.lister = reviews.reviewee
                            LEFT OUTER JOIN bids ON sales.sid = bids.sid
                    WHERE   sales.sid = ? COLLATE NOCASE
                    GROUP BY sales.lister, sales.sid;''', (selection,))
    print("********List all detailed information of sales selected********")
    column_title = [[]]
    for i in range(len(cursor.description)):
        column_title[0].append(cursor.description[i][0])
    reviews = cursor.fetchall()
    results = []
    for i in range(len(reviews)):
        results.append(list(reviews[i]))
    results = column_title + results
    print("|" + results[0][0].center(15) + "|", end="")
    print(results[0][1].center(20) + "|", end="")
    print(results[0][2].center(20) + "|", end="")
    print(results[0][3].center(30) + "|", end="")
    print(results[0][4].center(10) + "|", end="")
    print(results[0][5].center(10) + "|", end="")
    print(results[0][6].center(7) + "|")

    for i in range(1, len(results)):
        print("|" + str(results[i][0]).center(15) + "|", end="")
        print(str(results[i][1]).center(20) + "|", end="")
        print(str(results[i][2]).center(20) + "|", end="")
        print(str(results[i][3]).center(30) + "|", end="")
        print(str(results[i][4]).center(10) + "|", end="")
        print(str(results[i][5]).center(10) + "|", end="")
        print(str(results[i][6]).center(7) + "|")


def place_bid(conn, cursor, selection, current_user):
    # find the max bids amount in the database
    cursor.execute('''SELECT   case WHEN bids.amount is null
                                  then sales.rprice
                              ELSE max(bids.amount)
                            END status
                        FROM sales LEFT OUTER JOIN bids ON sales.sid = bids.sid
                        WHERE sales.sid = ? COLLATE NOCASE
                        GROUP BY sales.sid;''', (selection,))
    reviews = cursor.fetchall()
    max_bids = reviews[0][0]
    # check whether amount inputted is greater than the max amount
    bids_amount = int(input("Enter an amount for your bids: "))
    while max_bids > bids_amount:
        print("Your bids is smaller than the current maximum bids", max_bids)
        print("TRY ANOTHER ONE")
        print("bids: ", end="")
        bids_amount = int(input())

    cursor.execute('''SELECT sales.sid
                      FROM sales
                      WHERE sales.sid = ? COLLATE NOCASE;''', (selection, ))

    selection = cursor.fetchall()[0][0]

    # find unique bid for next insertion
    x = uuid.uuid4()
    cursor.execute('''INSERT INTO bids (bid, bidder, sid, bdate, amount) \
                      VALUES (?, ?, ?, ?, ?);''', (str(x)[:20], current_user, selection, strftime("%Y/%m/%d", gmtime()),
                                                   bids_amount))
    conn.commit()


def list_sales(cursor):
    cursor.execute('''SELECT    sales.sid,
                                sales.descr,
                                case WHEN bids.amount is null
                                      then sales.rprice
                                  ELSE max(bids.amount)
                                END status,
                                CAST((strftime('%s', sales.edate) - strftime('%s', 'now')) / (60 * 60 * 24) AS TEXT) || ' days ' ||
                                CAST(((strftime('%s', sales.edate) - strftime('%s', 'now')) % (60 * 60 * 24)) / (60 * 60) AS TEXT) || ':' ||
                                CAST((((strftime('%s', sales.edate) - strftime('%s', 'now')) % (60 * 60 * 24)) % (60 * 60)) / 60 AS TEXT) AS time
                        FROM sales LEFT OUTER JOIN bids ON sales.sid = bids.sid
                        WHERE sales.edate > DATE('now')
                        GROUP BY sales.sid
                        ORDER BY sales.edate ASC;''')
    column_title = [[]]
    for i in range(len(cursor.description)):
        column_title[0].append(cursor.description[i][0])
    reviews = cursor.fetchall()
    results = []
    for i in range(len(reviews)):
        results.append(list(reviews[i]))
    results = column_title + results

    return results


def list_reviews(cursor, selection):
    cursor.execute('''SELECT reviews.reviewer, reviews.reviewee, reviews.rating, reviews.rtext, reviews.rdate
                    FROM    reviews, sales
                    WHERE   reviews.reviewee = sales.lister
                    AND     sales.sid = ? COLLATE NOCASE;''', (selection,))
    column_title = [[]]
    for i in range(len(cursor.description)):
        column_title[0].append(cursor.description[i][0])
    reviews = cursor.fetchall()
    results = []
    for i in range(len(reviews)):
        results.append(list(reviews[i]))
    results = column_title + results

    return results

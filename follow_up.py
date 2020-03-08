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
    cursor.execute('''SELECT  sales.lister,
                            COUNT(reviews.reviewer) as number_of_ratings, AVG(reviews.rating) as average_rating,
                            sales.descr, sales.edate, sales.cond,
                            case bids.amount
                                WHEN not null 
                                    then max(bids.amount)
                                ELSE sales.rprice
                            END status
                    FROM    sales LEFT OUTER JOIN reviews ON sales.lister = reviews.reviewee
                            LEFT OUTER JOIN bids ON sales.sid = bids.sid
                    WHERE   sales.sid = ?
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
    print("|" + results[0][0].center(5) + "|", end="")
    print(results[0][1].center(5) + "|", end="")
    print(results[0][2].center(5) + "|", end="")
    print(results[0][3].center(40) + "|", end="")
    print(results[0][4].center(10) + "|", end="")
    print(results[0][5].center(16) + "|", end="")
    print(results[0][6].center(5) + "|")

    for i in range(1, len(results)):
        print("|" + str(results[i][0]).center(5) + "|", end="")
        print(str(results[i][1]).center(5) + "|", end="")
        print(str(results[i][2]).center(5) + "|", end="")
        print(str(results[i][3]).center(40) + "|", end="")
        print(str(results[i][4]).center(10) + "|", end="")
        print(str(results[i][5]).center(16) + "|", end="")
        print(str(results[i][6]).center(5) + "|")


def place_bid(conn, cursor, selection, current_user):
    # find the max bids amount in the database
    cursor.execute('''SELECT  case bids.amount
                                WHEN null 
                                    then sales.rprice
                                ELSE max(bids.amount)
                            END status
                    FROM    sales LEFT OUTER JOIN bids ON sales.sid = bids.sid
                    WHERE sales.sid = ?
                    GROUP BY sales.sid;''', (selection,))
    reviews = cursor.fetchall()
    max_bids = reviews[0][0]
    print(max_bids)
    # check whether amount inputted is greater than the max amount
    bids_amount = int(input())
    while max_bids > bids_amount:
        bids_amount = int(input())
    # find unique bid for next insertion
    x = uuid.uuid4()
    cursor.execute('''INSERT INTO bids (bid, bidder, sid, bdate, amount) \
                      VALUES (?, ?, ?, ?, ?);''', [str(x)[:20], current_user, selection, strftime("%Y/%m/%d", gmtime()),
                                                   bids_amount])
    conn.commit()


def list_sales(cursor):
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
    cursor.execute('''SELECT  reviews.rtext as review_text 
                    FROM    reviews, sales
                    WHERE   reviews.reviewee = sales.lister
                    AND     sales.sid = ?;''', (selection,))
    column_title = [[]]
    for i in range(len(cursor.description)):
        column_title[0].append(cursor.description[i][0])
    reviews = cursor.fetchall()
    results = []
    for i in range(len(reviews)):
        results.append(list(reviews[i]))
    results = column_title + results

    return results


if __name__ == "__main__":
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    # display_information(cursor, 'S01')
    # place_bid(conn, cursor, 'S01', 'qianqiu@ualberta.ca')
    results = list_reviews(cursor, 'S02')
    print("|" + results[0][0].center(40) + "|")
    for i in range(1, len(results)):
        print("|" + str(results[i][0]).center(40) + "|")
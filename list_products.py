import sqlite3


# ********List qualifying products information********
def list_products(cursor):
    cursor.execute('''SELECT products.pid, products.descr, COUNT(DISTINCT previews.rid) AS number_of_reviews, \
                      AVG(previews.rating) AS average_rating, COUNT(DISTINCT sales.sid) AS number_of_active_sales \
                      FROM (products LEFT OUTER JOIN sales ON products.pid = sales.pid) \
                      LEFT OUTER JOIN previews ON products.pid = previews.pid \
                      WHERE sales.edate > DATE('now') \
                      GROUP BY products.pid \
                      ORDER BY number_of_active_sales DESC;''')
    return cursor.fetchall()


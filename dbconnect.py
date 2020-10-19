import MySQLdb

def connection():
    conn = MySQLdb.connect(host='localhost',
                            user='root',
                            passwd='Logan@6824',
                            db='MoneyLine')
    c = conn.cursor()
    return c, conn
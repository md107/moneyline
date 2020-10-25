import MySQLdb

def connection():
    conn = MySQLdb.connect(host='localhost',
                            user='root',
                            passwd='PASSWORD',
                            db='MoneyLine')
    c = conn.cursor()
    return c, conn
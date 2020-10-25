import MySQLdb

def connection():
    conn = MySQLdb.connect(host='localhost',
                            user='csds393',
                            passwd='moneyline',
                            db='MoneyLine')
    c = conn.cursor()
    return c, conn
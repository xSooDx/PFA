import gc
import MySQLdb
db_host = "localhost"
db_name = 'pfa'
db_user = 'pfa'
db_pass = '123456'
user_table = 'user'
debt_table = 'debt'
transaction_table = 'transaction'

def DBclose(c, conn):
    c.close()
    conn.close()
    gc.collect()


def DBconnect():
    conn = MySQLdb.connect(
        host=db_host,
        user=db_user,
        passwd=db_pass,
        db=db_name,
    )
    c = conn.cursor(MySQLdb.cursors.DictCursor)

    return c, conn
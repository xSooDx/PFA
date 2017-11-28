import dbManager as dbm
import MySQLdb


def testCredentials(username, password):
    c, conn = dbm.DBconnect()
    c.execute("SELECT * from user where username = '{}' and password = '{}'".format(username, password))
    res = c.fetchall()
    dbm.DBclose(c, conn)
    if len(res) == 1:
        return True, res
    return False, None


def registerUser(username, password):
    c, conn = dbm.DBconnect()

    try:
        c.execute("INSERT into user(username,password) Values('{}', '{}')".format(username, password))
        conn.commit()
        dbm.DBclose(c, conn)
        return True
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        dbm.DBclose(c, conn)
        return False

def updateIncome(userID, income):
    pass
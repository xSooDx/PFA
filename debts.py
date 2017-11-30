import dbManager as dbm
import MySQLdb


def insertIntoDebt(user_id, amount, income, name, participant, category, timestamp,duedate):
    c, conn = dbm.DBconnect();
    # time = str(timestamp)
    try:
        s = "INSERT into debt(user_id, amount, income, name, participant, category, timestamp,duedate) values({},{},{},'{}', '{}', '{}','{}','{}');".format(
            user_id, amount, income, name, participant, category, timestamp, duedate)
        c.execute(s)
        conn.commit()
        dbm.DBclose(c, conn)
        return True
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        dbm.DBclose(c, conn)
        return False


def readFromDebt(user_id):
    c, conn = dbm.DBconnect()
    try:
        s = "Select * from debt where user_id = {} order by timestamp desc ".format(user_id)
        # print(s)
        c.execute(s)
        result = c.fetchall()
        conn.commit()
        dbm.DBclose(c, conn)
        return result
    except(MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        dbm.DBclose(c, conn)


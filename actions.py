from flask import session
from users import *
from transaction import *
from debts import *


def __set_login_session(username, id):
    session['username'] = username
    session['logged_in'] = True
    session['id'] = id


def login(username, password):
    c, user = testCredentials(username, password)
    if c:
        __set_login_session(username, user['id'])
        return True

    else:
        return False


def register(username, password):
    if registerUser(username, password):
        return login(username, password)
    else:
        return False


def logout():
    session['logged_in'] = False
    session['username'] = None


def getTransactions(user_id):
    ts = readFromTransaction(user_id)
    if ts:
        for i in ts:
            i['date'] = i['timestamp'].date()
            i['time'] = i['timestamp'].time()
    else: ts = None
    return ts


def addTransactions(user_id, amount, income, name, participant, category, timestamp):
    if income == "true":
        income = True
    else:
        income = False
    insertIntoTransaction(user_id, amount, income, name, participant, category, timestamp)


def getDebts(user_id):
    ts = readFromDebt(user_id)
    if ts:
        for i in ts:
            i['date'] = i['timestamp'].date()
            i['time'] = i['timestamp'].time()
    else: ts = None
    return ts


def addDebt(user_id, amount, income, name, participant, category, timestamp, duedate):
    if income == "true":
        income = True
    else:
        income = False
    insertIntoDebt(user_id, amount, income, name, participant, category, timestamp, duedate)

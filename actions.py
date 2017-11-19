from flask import session
from users import *


def __set_login_session(username):
    session['username'] = username
    session['logged_in'] = True


def login(username, password):
    c , user = testCredentials(username, password)
    if c :
        __set_login_session(username)
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

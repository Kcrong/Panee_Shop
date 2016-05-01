from flask import session

from app.static_string import json_message


def login_required(func):
    def check_login(*args, **kwargs):
        if session['login'] is True:
            func(*args, **kwargs)
        else:
            return json_message("Login Required", 401)

    return check_login


def logout_required(func):
    def check_logout(*args, **kwargs):
        if session['login'] is True:
            func(*args, **kwargs)
        else:
            return json_message("Logout Required", 401)

    return check_logout


def login_user(userid):
    session['login'] = True
    session['userid'] = userid


def logout_user():
    session['login'] = False
    session['userid'] = None

from flask import session

from app.static_string import json_message


def login_required(func):
    def newFunc(*args, **kwargs):
        if session['login'] is True:
            func(*args, **kwargs)
        else:
            return json_message("Login Required", 401)

    return newFunc


def login_user(userid):
    session['login'] = True
    session['userid'] = userid


def logout_user():
    session['login'] = False
    session['userid'] = None

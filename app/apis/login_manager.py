from flask import session

from app.models import Users
from app.static_string import json_message


def login_required(func):
    def check_login(*args, **kwargs):
        try:
            session['login']
        except KeyError:
            session['login'] = False
        finally:
            if session['login'] is True:
                return func(*args, **kwargs)
            else:
                return json_message("Login Required", 401)

    return check_login


def logout_required(func):
    def check_logout(*args, **kwargs):
        try:
            session['login']
        except KeyError:
            session['login'] = False
        finally:
            if session['login'] is False:
                return func(*args, **kwargs)
            else:
                return json_message("Logout Required", 401)

    return check_logout


def login_user(userid):
    session['login'] = True
    session['userid'] = userid


def logout_user():
    session['login'] = False
    session['userid'] = None


def current_user():
    u = Users.query.filter_by(userid=session['userid']).first()
    return u

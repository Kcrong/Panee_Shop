#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import request
from flask_restful import Resource, reqparse

from app.static_string import USER_LOGIN_URL, USER_LOGOUT_URL, USER_REGISTER_URL
from config import USE_METHOD, DEBUG
from . import user_api
from app.models import User, db
from app.static_string import json_message
from .login_manager import login_required, login_user, logout_user, logout_required
from sqlalchemy.exc import IntegrityError


@user_api.resource(USER_LOGIN_URL)
class Login(Resource):
    def __init__(self):
        self.parser = user_parser[USER_LOGIN_URL][request.method]
        self.args = self.parser.parse_args()

    @logout_required
    def post(self):
        args = self.args
        u = User.query.filter_by(userid=args['userid'], userpw=args['userpw'], active=True).first()
        if u is None:
            return json_message('Invalid ID or PW', 400)
        else:
            login_user(u.userid)
            return json_message()


@user_api.resource(USER_LOGOUT_URL)
class Logout(Resource):
    @login_required
    def get(self):
        logout_user()
        return json_message()


@user_api.resource(USER_REGISTER_URL)
class Register(Resource):
    def __init__(self):
        self.parser = user_parser[USER_REGISTER_URL][request.method]
        self.args = self.parser.parse_args()

    @logout_required
    def post(self):
        args = self.args
        u = User(args['userid'], args['userpw'], args['name'], args['email'], args['nickname'])

        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()

            if DEBUG:
                dup = e.args[0].split(':')[1].split('.')[1]
            else:
                dup = e.message.split('for key')[1].split("'")[1]
            message = "%s is duplicate" % dup

            return json_message(message, 400)

        else:
            return json_message()


user_parser = {
    resource[1][0]: {method: reqparse.RequestParser() for method in USE_METHOD}
    for resource in user_api.resources
    }

# USER_LOGIN - POST
parser = user_parser[USER_LOGIN_URL]['POST']
parser.add_argument('userid', type=str, help='Need String Userid', required=True)
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)

# USER_LOGOUT - POST
parser = user_parser[USER_LOGOUT_URL]['POST']
parser.add_argument('userid', type=str, help='Need String Userid', required=True)
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)

# USER_REGISTER - POST
parser = user_parser[USER_REGISTER_URL]['POST']
parser.add_argument('userid', type=str, help='Need String Userid', required=True)
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)
parser.add_argument('name', type=str, help='Need String name', required=True)
parser.add_argument('email', type=str, help='Need String email', required=True)
parser.add_argument('nickname', type=str, help='Need String nickname', required=True)

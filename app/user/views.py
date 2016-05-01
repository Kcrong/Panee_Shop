#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import request
from flask_restful import Resource, reqparse

from app.static_string import USER_LOGIN_URL, USER_LOGOUT_URL
from config import USE_METHOD
from . import user_api
from app.models import User
from app.static_string import json_message
from .login_manager import login_required, login_user, logout_user


@user_api.resource(USER_LOGIN_URL)
class Login(Resource):
    def __init__(self):
        self.parser = user_parser[USER_LOGIN_URL][request.method]

    def get(self):
        login_user('asdf')
        return json_message()

    @login_required
    def post(self):
        args = self.parser.parse_args()
        u = User.query.filter_by(userid=args['userid'], userpw=args['userpw'], active=True).first_or_404()


@user_api.resource(USER_LOGOUT_URL)
class Logout(Resource):

    @login_required
    def get(self):
        logout_user()
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

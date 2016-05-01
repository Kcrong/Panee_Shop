#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import request
from flask_restful import Resource, reqparse

from app.static_string import USER_LOGIN_URL, USER_LOGOUT_URL
from config import USE_METHOD
from . import user_api


@user_api.resource(USER_LOGIN_URL)
class Login(Resource):
    def __init__(self):
        self.parser = user_parser[request.method]

    def get(self):
        """
        Logout User
        """
        return user_parser.parse_args()

    def post(self):
        return self.parser.args[0].name


@user_api.resource(USER_LOGOUT_URL)
class Logout(Resource):
    def __init__(self):
        self.parser = user_parser[request.method]

    def get(self):
        return "User Logout"


user_parser = {
    resource[1][0]: {method: reqparse.RequestParser() for method in USE_METHOD}
    for resource in user_api.resources
    }

# USER_LOGIN - POST
parser = user_parser[USER_LOGIN_URL]['POST']
parser.add_argument('userid', type=str, help='Need Userid')

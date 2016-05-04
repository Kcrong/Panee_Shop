#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import request
from flask_restful import Resource, reqparse

from app.models import User, db
from app.static_string import USER_MAIN_URL, USER_SESSION_URL
from app.static_string import json_message

from sqlalchemy.exc import IntegrityError

from config import USE_METHOD

from . import user_api
from .login_manager import login_required, current_user, logout_required, login_user, logout_user


@user_api.resource(USER_MAIN_URL)
class Main(Resource):
    def __init__(self):
        self.parser = user_parser[USER_MAIN_URL][request.method]
        self.args = self.parser.parse_args()

    def get(self):
        args = self.args
        u = User.query.filter_by(userid=args['userid'], active=True).first_or_404()
        return u.base_info_dict

    @login_required
    def delete(self):
        u = current_user()
        if u.userpw != self.args['userpw']:
            return json_message('Diff password', 401)
        else:
            u.active = False
            db.session.commit()
            logout_user()
            return json_message()

    @logout_required
    def post(self):
        args = self.args
        u = User(args['userid'], args['userpw'], args['name'], args['email'], args['nickname'])

        db.session.add(u)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()

            try:
                dup = e.message.split('for key')[1].split("'")[1]
            except AttributeError:
                dup = e.args[0].split(':')[1].split('.')[1]

            message = "%s is duplicate" % dup

            return json_message(message, 400)

        else:
            return json_message()


@user_api.resource(USER_SESSION_URL)
class Session(Resource):
    def __init__(self):
        self.parser = user_parser[USER_SESSION_URL][request.method]
        self.args = self.parser.parse_args()

    @login_required
    def get(self):
        u = current_user()
        return u.base_info_dict

    @logout_required
    def post(self):
        args = self.args
        u = User.query.filter_by(userid=args['userid'], userpw=args['userpw'], active=True).first_or_404()
        login_user(u.userid)
        return json_message()

    @login_required
    def delete(self):
        logout_user()
        return json_message()


user_parser = {
    resource[1][0]: {method: reqparse.RequestParser() for method in USE_METHOD}
    for resource in user_api.resources
    }

# USER_MAIN - GET : 현재 사용자 정보
parser = user_parser[USER_MAIN_URL]['GET']
parser.add_argument('userid', type=str, help='Need String Userid', required=True)

# USER_MAIN - POST: 사용자 등록 (회원가입)
parser = user_parser[USER_MAIN_URL]['POST']
parser.add_argument('userid', type=str, help='Need String Userid', required=True)
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)
parser.add_argument('name', type=str, help='Need String name', required=True)
parser.add_argument('email', type=str, help='Need String email', required=True)
parser.add_argument('nickname', type=str, help='Need String nickname', required=True)

# USER_MAIN - GETS: 회원들 정보??
" Can't understand"

# USER_MAIN - DELETE: 회원탈퇴
parser = user_parser[USER_MAIN_URL]['DELETE']
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)

# USER_SESSION - GET: 접속중인 사용자
"NO required args"

# USER_SESSION - POST: 로그인
parser = user_parser[USER_SESSION_URL]['POST']
parser.add_argument('userid', type=str, help='Need String Userid', required=True)
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)

# USER_SESSION - DELETE: 로그아웃
"NO required args"

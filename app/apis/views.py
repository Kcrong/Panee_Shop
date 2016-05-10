#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import request
from sqlalchemy.exc import IntegrityError

from app import RestBase
from app.models import User, db
from app.static_string import APIS_ACCOUNT_URL, APIS_SESSION_URL
from app.static_string import json_message
from . import main_api
from .login_manager import login_required, current_user, logout_required, login_user, logout_user


@main_api.resource(APIS_ACCOUNT_URL)
class Main(RestBase):
    def __init__(self):
        self.parser = apis_parser[APIS_ACCOUNT_URL][request.method]

    def get(self):
        args = self.args
        u = User.query.filter_by(id=args['userid'], active=True).first_or_404()
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


@main_api.resource(APIS_SESSION_URL)
class Session(RestBase):
    def __init__(self):
        self.parser = apis_parser[APIS_SESSION_URL][request.method]

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


from .arg_manager import apis_parser

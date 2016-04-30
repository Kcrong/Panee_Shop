#!/usr/bin/env python
# -*- coding:utf-8 -*-
from . import user_blueprint, user_api
from flask_restful import Resource


@user_blueprint.route('/')
def hello_user():
    return "Hello User"


@user_api.resource('/test')
class Test(Resource):
    def get(self):
        return "User Hello"

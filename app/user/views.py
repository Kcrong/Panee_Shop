#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource
from flask import request

from . import user_api, user_parser

parser = user_parser['POST']
parser.add_argument('userid', type=str, help='Need Userid')


@user_api.resource('/login')
class Login(Resource):
    def __init__(self):
        self.parser = user_parser[request.method]

    def get(self):
        return user_parser.parse_args()

    def post(self):
        return self.parser.args[0].name

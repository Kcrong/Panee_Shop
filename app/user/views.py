#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource

from . import user_api, user_parser


@user_api.resource('/login')
class Login(Resource):
    def get(self):
        return user_parser.parse_args()

    def post(self):
        user_parser.add_argument('userid', type=str, help='Only Int!')
        return user_parser.parse_args()

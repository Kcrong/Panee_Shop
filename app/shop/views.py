#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from flask import request

from . import shop_api
from config import USE_METHOD
from app.static_string import SHOP_LIST_URL


@shop_api.resource(SHOP_LIST_URL)
class Shop(Resource):
    def __init__(self):
        self.parser = shop_parser[SHOP_LIST_URL][request.method]

    def get(self):
        return "Shop GET"

    def post(self):
        args = self.parser.parse_args()
        return args


shop_parser = {
    resource[1][0]: {method: reqparse.RequestParser() for method in USE_METHOD}
    for resource in shop_api.resources
    }

# USER_LOGIN - POST
parser = shop_parser[SHOP_LIST_URL]['POST']
parser.add_argument('name', type=str, help='Need Shop Item name')
parser.add_argument('price', type=int, help='Need Shop Item price')

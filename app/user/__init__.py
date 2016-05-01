#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask_restful import Api, reqparse
from config import USE_METHOD

user_blueprint = Blueprint('user', __name__)
user_api = Api(user_blueprint)
user_parser = {method: reqparse.RequestParser() for method in USE_METHOD}

from . import views

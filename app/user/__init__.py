#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask_restful import Api, reqparse

user_blueprint = Blueprint('user', __name__)
user_api = Api(user_blueprint)
user_parser = reqparse.RequestParser()

from . import views

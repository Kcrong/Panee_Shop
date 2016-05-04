#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from app.static_string import *

user_api = Api()
user_blueprint = Blueprint(USER_NAME, __name__)

user_api.init_app(user_blueprint)

from .views import *

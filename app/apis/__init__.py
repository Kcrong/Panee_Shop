#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from app.static_string import *

main_api = Api()
apis_blueprint = Blueprint(APIS_NAME, __name__)

main_api.init_app(apis_blueprint)

from .views import *

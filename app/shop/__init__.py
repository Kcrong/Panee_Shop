#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from app.static_string import SHOP_NAME

shop_api = Api()
shop_blueprint = Blueprint(SHOP_NAME, __name__)

shop_api.init_app(shop_blueprint)

from . import views
from .views import *

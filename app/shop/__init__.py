#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

shop_blueprint = Blueprint('shop', __name__)

from . import views
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from app.static_string import *

explorer_blueprint = Blueprint(EXPLORER_NAME, __name__,
                               template_folder=EXPLORER_TEMPLATE_PATH)

from . import views

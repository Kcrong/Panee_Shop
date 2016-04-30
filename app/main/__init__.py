#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
import os.path

main_blueprint = Blueprint('main', __name__)

from . import views

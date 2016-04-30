#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

from flask import Blueprint

template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../', 'client')
main_blueprint = Blueprint('main', __name__, template_folder=template_path)

from . import views

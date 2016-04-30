#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, send_from_directory, url_for
import os.path

from . import main_blueprint

static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../', 'client', 'app')


@main_blueprint.route('/index')
def index():
    return render_template('index.html')

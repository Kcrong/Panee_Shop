#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, send_from_directory

from . import main_blueprint
from config import STATIC_FOLDER


@main_blueprint.route('/')
def index():
    return render_template('index.html')


@main_blueprint.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(STATIC_FOLDER, filename)

#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import send_from_directory, redirect, url_for
from flask.ext.login import login_required
from . import main_blueprint


@main_blueprint.route('/')
@login_required
def index():
    return redirect(url_for('shop.product_list'))


@main_blueprint.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(main_blueprint.root_path + '/../static/css/', filename)


@main_blueprint.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(main_blueprint.root_path + '/../static/js/', filename)


@main_blueprint.route('/image/<path:filename>')
def img_static(filename):
    return send_from_directory(main_blueprint.root_path + '/../static/image/', filename)


@main_blueprint.route('/font/<path:filename>')
def font_static(filename):
    return send_from_directory(main_blueprint.root_path + '/../static/font/', filename)

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

from flask import render_template, send_from_directory

from app.static_string import EXPLORER_STATIC_PATH, EXPLORER_STATIC_URL
from . import explorer_blueprint

# Import All blueprint
import app.apis

all_module_dict = dict()
apis_path = app.apis.__path__[0]
module_list = [name for name in os.listdir(apis_path)
               if "__" not in name and os.path.isdir(os.path.join(apis_path, name))]

# [name for name in os.listdir(apis_path) if os.path.isdir(os.path.join(apis_path, name))] == ['Files', 'Users']
for module in module_list:
    all_module_dict[module] = getattr(app.apis, module)

template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
template_name = os.listdir(template_path)[0]


@explorer_blueprint.route(EXPLORER_STATIC_URL + '/<path:filename>')
def static_files(filename):
    return send_from_directory(EXPLORER_STATIC_PATH, filename)


@explorer_blueprint.route('/')
@explorer_blueprint.route('/<string:blueprint>/<string:api>')
def index(blueprint=None, api=None):
    if blueprint is None or api is None:
        blueprint, module = list(all_module_dict.items())[0]
        api = module.api.resources[0][1][0]

    api_class = [api_class for api_class, url, _ in all_module_dict[blueprint].api.resources
                 if api in url[0]][0]

    return render_template(template_name,
                           blueprint=blueprint,
                           api=api,
                           api_class=api_class,
                           all_module=all_module_dict)

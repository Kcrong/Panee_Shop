#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, send_from_directory, redirect, url_for

from . import explorer_blueprint

from app.static_string import EXPLORER_STATIC_PATH, EXPLORER_INDEX_URL, EXPLORER_URL_PREFIX

# Import All blueprint
from app.apis.File import file_blueprint, file_api, file_api_parser
from app.apis.User import user_api_parser, user_blueprint, user_api

API_DICT = {
    # (api, parser, blueprint)
    file_blueprint.name: (file_api, file_api_parser, file_blueprint),
    user_blueprint.name: (user_api, user_api_parser, user_blueprint)
}


@explorer_blueprint.route('/')
def redirect_index():
    api_list = list(API_DICT.values())
    return redirect(url_for('.index',
                            blueprint=api_list[0][2].name,
                            api=api_list[0][0].resources[0][1][0][1:],
                            method='GET'))


@explorer_blueprint.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(EXPLORER_STATIC_PATH, filename)


@explorer_blueprint.route(EXPLORER_INDEX_URL + '/<string:blueprint>/<string:api>/<string:method>')
def index(blueprint, api, method):
    api_resource_index = [url[0] for api_class, url, _ in API_DICT[blueprint][0].resources].index('/' + api)
    method_list = API_DICT[blueprint][0].resources[api_resource_index][0].methods

    return render_template('explorer.html',
                           base_url=EXPLORER_URL_PREFIX + EXPLORER_INDEX_URL,
                           api_list=API_DICT,
                           req_blueprint=blueprint,
                           req_api=api,
                           req_method=method,
                           method_list=method_list)

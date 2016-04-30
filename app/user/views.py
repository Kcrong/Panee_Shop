#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import user_blueprint


@user_blueprint.route('/')
def index():
    return "User Index"

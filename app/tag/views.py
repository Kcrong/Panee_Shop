#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from . import tag_blueprint

from ..models import *


@tag_blueprint.route('/list')
def taglist():
    all_tag = Tag.query.filter_by(top=True).all()

    return json.dumps([tag.name for tag in all_tag])

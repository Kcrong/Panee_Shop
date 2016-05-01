#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask.ext.script import Manager

app = Flask(__name__)


def create_app():
    from .main import main_blueprint
    from .user import user_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/user')

    app.config.from_pyfile('../config.py')

    return app

manager = Manager(app)

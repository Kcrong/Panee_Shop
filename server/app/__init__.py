#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import os

from flask import Flask, redirect, url_for
from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

try:
    import MySQLdb
except ImportError:
    import pymysql
    pymysql.install_as_MySQLdb()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

"""
3초만에 API를 이해하고, 30초만에 API 키를 발급 받아서,
3분안에 첫번째 요청이 오도록 해라
"""

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()


def setting_app():
    from .main import main_blueprint
    from .user import user_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/user')

    app.static_folder = os.path.join(app.root_path, '../../', 'client', 'app')

    app.config.from_pyfile('../config.py')

    return app


db.init_app(app)

from .models import *

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, session
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand

try:
    import MySQLdb
except ImportError:
    import pymysql

    pymysql.install_as_MySQLdb()

from .static_string import *

app = Flask(__name__)
db = SQLAlchemy()


def setting_session():
    session['login'] = False
    session['userid'] = None


def create_app():
    from .main import main_blueprint
    from .user import user_blueprint
    from .shop import shop_blueprint
    from .api_explorer import explorer_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint, url_prefix=USER_URL_PREFIX)
    app.register_blueprint(shop_blueprint, url_prefix=SHOP_URL_PREFIX)
    app.register_blueprint(explorer_blueprint, url_prefix=EXPLORER_URL_PREFIX)

    app.config.from_pyfile('../config.py')

    app.before_first_request(setting_session)

    return app


manager = Manager(app)
manager.add_command('db', MigrateCommand)

db.init_app(app)

from .models import *

migrate = Migrate(app, db)

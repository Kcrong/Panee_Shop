#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, session
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask_restful import Resource
from werkzeug.datastructures import FileStorage

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
    from .apis import apis_blueprint
    from .api_explorer import explorer_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(apis_blueprint, url_prefix=APIS_URL_PREFIX)
    app.register_blueprint(explorer_blueprint, url_prefix=EXPLORER_URL_PREFIX)

    app.config.from_pyfile('../config.py')

    app.before_first_request(setting_session)

    return app


manager = Manager(app)
manager.add_command('db', MigrateCommand)

db.init_app(app)

from .models import *

migrate = Migrate(app, db)


class RestBase(Resource):
    @property
    def args(self):
        return self.parser.parse_args()


type_dict = {
    FileStorage: 'file',
    str: 'text',
    int: 'number'
}


@app.template_filter('totype')
def class2input(class_obj):
    return type_dict[class_obj]

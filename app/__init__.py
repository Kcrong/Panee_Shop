#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging

from flask import Flask, redirect, url_for
from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

"""
3초만에 API를 이해하고, 30초만에 API 키를 발급 받아서,
3분안에 첫번째 요청이 오도록 해라
"""

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()


def setting_app():
    from app.main import main_blueprint
    from app.user import user_blueprint
    from app.shop import shop_blueprint
    from app.tag import tag_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(shop_blueprint, url_prefix='/shop')
    app.register_blueprint(tag_blueprint, url_prefix='/tag')

    app.config.from_pyfile('../config.py')

    return app


app = setting_app()
db = SQLAlchemy(app)

from app.models import *

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.errorhandler(401)
def need_login(error):
    return redirect(url_for('user.login'))


@manager.command
def init_db():
    u1 = User('testid1', 'testpw', '010-1234-1231', '홍길동', 'nick1', 'access_token', 'facebook_id')
    db.session.add(u1)
    u2 = User('testid2', 'testpw', '010-1234-1232', '홍길동', 'nick2', 'access_token', 'facebook_id2')
    db.session.add(u2)
    u3 = User('testid3', 'testpw', '010-1234-1233', '홍길동', 'nick3', 'access_token', 'facebook_id3')
    db.session.add(u3)
    u4 = User('testid4', 'testpw', '010-1234-1234', '홍길동', 'nick4', 'access_token', 'facebook_id4')
    db.session.add(u4)

    db.session.add_all([u1, u2, u3, u4])

    t1 = Tag('piano')
    t2 = Tag('music')
    t3 = Tag('movie')
    t4 = Tag('dance')

    db.session.add_all([u1, u2, u3, u4, t1, t2, t3, t4])

    p1 = Product('product1', u1, 3000)
    p2 = Product('product2', u2, 3001)
    p3 = Product('product3', u3, 3002)
    p4 = Product('product4', u4, 3003)

    p1.tag.append(t1)
    p2.tag.append(t2)
    p3.tag.append(t3)
    p4.tag.append(t4)

    db.session.add_all([p1, p2, p3, p4])

    c1 = Comment('comment1', u1)
    c2 = Comment('comment2', u2)
    c3 = Comment('comment3', u3)
    c4 = Comment('comment4', u4)

    db.session.add_all([c1, c2, c3, c4])

    p1.comment.append(c1)
    p2.comment.append(c2)
    p3.comment.append(c3)
    p4.comment.append(c4)

    p1.like.append(u1)
    p1.like.append(u2)
    p1.like.append(u3)
    p2.like.append(u1)
    p3.like.append(u2)
    p4.like.append(u3)
    p4.like.append(u4)

    db.session.commit()

    print('DB DUMMY')

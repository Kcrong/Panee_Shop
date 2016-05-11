#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from datetime import datetime

from app import db
from app.static_string import UPLOAD_PATH
from config import randomkey


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


class Files(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    original = db.Column(db.String(200), nullable=False)
    random = db.Column(db.String(200), nullable=False, unique=True)
    type = db.Column(db.String(10))

    def __init__(self, file):
        self.original = file.filename
        try:
            self.type = self.original.split('.')[-1]
        except IndexError:
            self.type = None

        self.random = randomkey(len(self.original)) + '.' + self.type

        file.save(self.save_path)

    def __del__(self):
        try:
            os.remove(self.save_path)
        except FileNotFoundError:
            pass

    @property
    def save_path(self):
        return os.path.join(UPLOAD_PATH, self.random)


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    userid = db.Column(db.String(50), unique=True, nullable=False)
    userpw = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    nickname = db.Column(db.String(50), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created = db.Column(db.DATETIME, default=datetime.now(), nullable=False)
    updated = db.Column(db.DATETIME, default=datetime.now(), nullable=False, onupdate=datetime.now())
    shop = db.relationship('Shop')

    def __init__(self, userid, userpw, name, email, nickname):
        self.userid = userid
        self.userpw = userpw
        self.name = name
        self.email = email
        self.nickname = nickname

    def __repr__(self):
        return "<User %s>" % self.userid

    @property
    def base_info_dict(self):
        return dict(userid=self.userid,
                    name=self.name,
                    email=self.email,
                    nickname=self.nickname,
                    created=self.created,
                    updated=self.updated)


class Shop(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    writer = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    def __init__(self, title):
        self.title = title

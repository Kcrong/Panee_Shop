#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime
from flask import jsonify

from app import db


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


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
        return jsonify(dict(userid=self.userid,
                            name=self.name,
                            email=self.email,
                            nickname=self.nickname,
                            created=self.created,
                            updated=self.updated))


class Shop(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    writer = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    def __init__(self, title):
        self.title = title

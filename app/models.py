#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app import db
from datetime import datetime


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

    def __init__(self, userid, userpw, name, email, nickname):
        self.userid = userid
        self.userpw = userpw
        self.name = name
        self.email = email
        self.nickname = nickname

    def __repr__(self):
        return "<User %s>" % self.userid

#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app import db


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    userid = db.Column(db.String(50), unique=True, nullable=False)
    userpw = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    nickname = db.Column(db.String(50), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, userid, userpw, name, email, nickname):
        self.userid = userid
        self.userpw = userpw
        self.name = name
        self.email = email
        self.nickname = nickname

    def __repr__(self):
        return "<User %s>" % self.userid

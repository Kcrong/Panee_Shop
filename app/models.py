#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from datetime import datetime
from contextlib import suppress

from app import db
from app.static_string import (
    UPLOAD_PATH,
    SMALL_IMAGE_SIZE,
    MEDIUM_IMAGE_SIZE,
    SMALL_IMAGE_NAME_HEADER,
    MEDIUM_IMAGE_NAME_HEADER
)
from config import randomkey

from PIL import Image


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
    is_image = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, file):
        self.original = file.filename
        try:
            self.type = self.original.split('.')[-1]
        except IndexError:
            self.type = None

        self.random = randomkey(len(self.original)) + '.' + self.type

        file.save(self.save_path)

        if Files.check_image(file):  # if file is image
            self.is_image = True

            small_image, medium_image = Files.resize_image(self.save_path)

            small_image_name = SMALL_IMAGE_NAME_HEADER + self.random
            medium_image_name = MEDIUM_IMAGE_NAME_HEADER + self.random

            small_image.save(Files.make_save_path(small_image_name))
            medium_image.save(Files.make_save_path(medium_image_name))

        else:
            self.is_image = False

    def delete(self):
        with suppress(FileNotFoundError):
            os.remove(self.save_path)
            if self.is_image:
                os.remove(Files.make_save_path(SMALL_IMAGE_NAME_HEADER + self.random))
                os.remove(Files.make_save_path(MEDIUM_IMAGE_NAME_HEADER + self.random))

        self.active = False

    @staticmethod
    def resize_image(image_path):
        im = Image.open(image_path)
        small = im.resize((int(im.size[0] * SMALL_IMAGE_SIZE),
                           int(im.size[1] * SMALL_IMAGE_SIZE)))

        medium = im.resize((int(im.size[0] * MEDIUM_IMAGE_SIZE),
                            int(im.size[1] * MEDIUM_IMAGE_SIZE)))

        return small, medium

    @staticmethod
    def check_image(file):
        try:
            filetype = file.filename.split('.')[-1].lower()
        except IndexError:
            filetype = ""
        finally:
            mimetype = file.mimetype.split('/')[0].lower()

        return mimetype == "image" or filetype in ['jpg', 'jpeg', 'png', 'gif', 'bmp']

    @staticmethod
    def make_save_path(filename):
        return os.path.join(UPLOAD_PATH, filename)

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

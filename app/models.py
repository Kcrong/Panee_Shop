# -*-coding: utf-8 -*-
from datetime import datetime

from flask.ext.login import UserMixin

from app import db

likes = db.Table('likes',
                 db.Column('person_id', db.INTEGER, db.ForeignKey('user.id')),
                 db.Column('product_id', db.INTEGER, db.ForeignKey('product.id'))
                 )


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


class Tag(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    shop_id = db.Column(db.INTEGER, db.ForeignKey('product.id'))
    top = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Tag %s>" % self.name


class User(db.Model, UserMixin):
    id = db.Column(db.INTEGER, primary_key=True)
    userid = db.Column(db.String(30), nullable=True, unique=True)
    userpw = db.Column(db.String(30), nullable=True)
    image = db.Column(db.String(50), default='default.png')
    phone = db.Column(db.String(15), nullable=True, unique=True)
    created = db.Column(db.DATETIME, default=datetime.now(), nullable=False)
    updated = db.Column(db.DATETIME, default=datetime.now(), nullable=False, onupdate=datetime.now())
    name = db.Column(db.String(30), nullable=True)
    nick = db.Column(db.String(30), nullable=True, unique=True)
    active = db.Column(db.Boolean, nullable=True, default=True)

    access_token = db.Column(db.String(255))
    fb_id = db.Column(db.String(20), unique=True)

    def __init__(self, userid=None, userpw=None, phone=None, name=None, nick=None, access_token=None, fb_id=None, image=None):
        self.userid = userid
        self.userpw = userpw
        self.phone = phone
        self.name = name
        self.nick = nick
        self.image = image
        self.access_token = access_token
        self.fb_id = fb_id

    def __repr__(self):
        return "<User %s>" % self.userid


class ProductImage(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    image = db.Column(db.String(100), nullable=False, unique=True)
    product_id = db.Column(db.INTEGER, db.ForeignKey('product.id'))

    def __init__(self, image):
        self.image = image


class Product(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    main_image = db.Column(db.String(50), default='default.png', nullable=False)
    image = db.relationship(ProductImage, backref='product')
    user = db.relationship(User, backref='product')
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    price = db.Column(db.INTEGER, nullable=False)
    tag = db.relationship(Tag, backref='product')
    comment = db.relationship('Comment', backref='product')
    like = db.relationship('User', secondary=likes,
                           backref='like_product')

    is_allow = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, name, user, price, is_allow=True):
        self.name = name
        self.user = user
        self.price = price
        self.is_allow = is_allow

    def __repr__(self):
        return "<Product %s>" % self.name

    @property
    def like_cnt(self):
        return len(self.like)


class Comment(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    content = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.INTEGER, db.ForeignKey('product.id'))
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    user = db.relationship(User, backref='comment')

    def __init__(self, content, user):
        self.content = content
        self.user = user

    def __repr__(self):
        return "<Comment %s>" % self.content

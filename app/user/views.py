#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import jsonify, send_from_directory, request, url_for, render_template, redirect
from flask.ext.login import login_user, login_required, current_user, logout_user
from sqlalchemy.exc import IntegrityError

from .fb_manager import *
from .naver_manager import *

from . import user_blueprint
from ..models import *


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    elif request.method == 'POST':
        u = User.query.filter_by(userid=request.form['userid'], userpw=request.form['userpw']).first()

        if u is None:
            return redirect(url_for('user.login'))

        else:

            u.authenticated = True
            login_user(u)

            return redirect(url_for('main.index'))


@user_blueprint.route('/idcheck')
def idcheck():
    dup = User.query.filter_by(userid=request.args['id']).first()
    if dup is None:
        return "true"
    else:
        return "false"


@user_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    logout_user()

    return jsonify({
        'success': True
    })


# For Static
@user_blueprint.route('/image/<path:filename>')
@login_required
def user_image(filename):
    return send_from_directory(user_blueprint.root_path + '/image/', filename)


@user_blueprint.route('/fb_login')
def facebook_login():
    return facebook.authorize(callback=url_for('user.facebook_authorized',
                                               next=request.args.get('next') or request.referrer or None,
                                               _external=True))


@user_blueprint.route('/fb_login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')

    me = facebook.get('/me')

    fb_user_id = me.data['id']
    access_token = resp['access_token']

    name = get_fb_user_name(fb_user_id, access_token)

    u = get_or_create(db.session, User, fb_id=me.data['id'], access_token=access_token, name=name)

    try:
        db.session.commit()
    except IntegrityError:
        # TODO: 기존 계정에 동일한 페이스북 계정이 연동되어 있을 경우, 우짤지 구현 해놓을 것
        return "dup!"

    save_all_fb_article(u)

    # TODO: redirect to main
    return redirect(url_for('main.index'))


@user_blueprint.route('/naver_login')
def naver_login():
    return ""


@user_blueprint.route('/naver_login/authorized')
def naver_authorized(resp):
    return ""

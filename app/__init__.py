#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, render_template, url_for, send_from_directory
from flask.ext.script import Manager

import os.path

app = Flask(__name__)
template_path = os.path.join(app.root_path, 'client', 'app')


def create_app():
    app.config.from_pyfile('../config.py')

    return app


@app.route('/index')
def testing():
    return render_template('index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(template_path, filename=filename)


manager = Manager(app)

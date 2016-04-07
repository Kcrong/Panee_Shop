#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from werkzeug.contrib.fixers import ProxyFix

from app import app, manager


# app.wsgi_app = ProxyFix(app.wsgi_app)

@manager.command
def run():
    app.run()


if __name__ == "__main__":
    manager.run()

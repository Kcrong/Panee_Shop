#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from werkzeug.contrib.fixers import ProxyFix
import os
import sys

# For Relative Import
sys.path.extend([os.path.dirname(os.path.abspath(__file__))])

from app import setting_app, manager

app = setting_app()


@manager.command
def run():
    app.run()


if __name__ == "__main__":
    manager.run()

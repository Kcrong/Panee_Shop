#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, manager

app = create_app()


@manager.command
def run():
    app.run()


if __name__ == "__main__":
    manager.run()

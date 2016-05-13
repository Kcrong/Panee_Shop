#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, manager, db

app = create_app()


@manager.command
def run():
    app.run()


@manager.command
def create_all():
    db.create_all()
    print("Complete")


if __name__ == "__main__":
    manager.run()

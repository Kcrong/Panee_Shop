#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import create_app, manager

app = create_app()


@manager.command
def run():
    app.run()


if __name__ == "__main__":
    manager.run()

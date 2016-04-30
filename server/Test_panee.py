# -*-coding: utf-8 -*-
import json
import unittest

from flask import url_for

import app
from app.models import *

from selenium import webdriver


class PaneelinTestCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    """
    Tag Test
    """

    def test_taglist(self):
        rv = self.app.get('/tag/list')

        for tag in Tag.query.filter_by(top=True).all():
            assert tag.name in rv.data.decode('utf-8')

    """
    Account Test
    """

    def login(self, userid, userpw):
        return self.app.post('/user/login', data=dict(
            userid=userid,
            userpw=userpw
        ), follow_redirects=False)

    def logout(self):
        return self.app.post('/user/logout', follow_redirects=False)

    def test_login_logout(self):

        # Block logout before login.
        rv = self.logout()
        assert 401 == rv.status_code

        # login correct user
        rv = self.login('testid1', 'testpw')
        try:
            assert 200 == rv.status_code
        except AssertionError:
            print(rv.status_code)
            raise

        assert '"success": true' in rv.data
        assert '"image":' in rv.data

        # logout
        rv = self.logout()
        assert 200 == rv.status_code
        assert '"success": true' in rv.data

        # login incorrect user
        rv = self.login('testidx', 'testpw')
        assert 404 == rv.status_code

    """
    Shop Test
    """

    def test_product_list(self):
        def search_product(name="", sort_type=""):
            def low_check(sorted_rv_json):
                return all(int(sorted_rv_json[i]['price']) <= int(sorted_rv_json[i + 1]['price']) for i in
                           range(len(sorted_rv_json) - 1))

            def high_check(sorted_rv_json):
                return all(int(sorted_rv_json[i]['price']) >= int(sorted_rv_json[i + 1]['price']) for i in
                           range(len(sorted_rv_json) - 1))

            def popular_check(sorted_rv_json):
                return all(int(sorted_rv_json[i]['like']) >= int(sorted_rv_json[i + 1]['like']) for i in
                           range(len(sorted_rv_json) - 1))

            url = '/shop/json/list/%s' % name

            rv = self.app.get(url, query_string=dict(sort=sort_type))

            try:
                assert rv.status_code == 200
            except AssertionError:
                print(rv.status_code)
                raise

            rv_json = json.loads(rv.data.decode('utf-8'))
            assert len(rv_json) > 0

            # json 특성상, 값 순서가 바뀌므로 order 값에 따라 정렬해준다.
            sorted_rv_json = sorted(rv_json, key=lambda x: x['order'])

            check_type = {
                '': popular_check,
                'low': low_check,
                'high': high_check,
                'popular': popular_check
            }

            return check_type[sort_type](sorted_rv_json)

        assert search_product(sort_type='')
        assert search_product(sort_type='low')
        assert search_product(sort_type='high')
        assert search_product(sort_type='popular')

if __name__ == '__main__':
    unittest.main()

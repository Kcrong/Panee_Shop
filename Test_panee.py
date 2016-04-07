# -*-coding: utf-8 -*-
import json
import unittest

import app
from app.models import *


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
            assert tag.name in rv.data

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
            print rv.status_code
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

    def low_check(self, sorted_rv_json):
        return all(int(sorted_rv_json[i]['price']) <= int(sorted_rv_json[i + 1]['price']) for i in
                   xrange(len(sorted_rv_json) - 1))

    def high_check(self, sorted_rv_json):
        return all(int(sorted_rv_json[i]['price']) >= int(sorted_rv_json[i + 1]['price']) for i in
                   xrange(len(sorted_rv_json) - 1))

    def popular_check(self, sorted_rv_json):
        return all(int(sorted_rv_json[i]['like']) >= int(sorted_rv_json[i + 1]['like']) for i in
                   xrange(len(sorted_rv_json) - 1))

    def search_product(self, name="", sort_type=""):

        url = '/shop/list/%s' % name

        rv = self.app.get(url, query_string=dict(sort=sort_type))

        try:
            assert rv.status_code == 200
        except AssertionError:
            print rv.status_code
            raise

        rv_json = json.loads(rv.data)
        assert len(rv_json) > 0

        # json 특성상, 값 순서가 바뀌므로 order 값에 따라 정렬해준다.
        sorted_rv_json = sorted(rv_json, key=lambda x: x['order'])

        check_type = {
            '': self.popular_check,
            'low': self.low_check,
            'high': self.high_check,
            'popular': self.popular_check
        }

        return check_type[sort_type](sorted_rv_json)

    def test_product_list(self):
        assert self.search_product(sort_type='')
        assert self.search_product(sort_type='low')
        assert self.search_product(sort_type='high')
        assert self.search_product(sort_type='popular')


if __name__ == '__main__':
    unittest.main()

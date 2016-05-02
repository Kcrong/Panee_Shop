# -*-coding: utf-8 -*-
from flask.ext.testing import TestCase, LiveServerTestCase

from app.models import *
from manage import app
from urllib import request

from app.static_string import *


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['SECRET_KEY'] = 'development-test-key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # + join(test_cwd, 'flask-tracking.db')
        app.config['TESTING'] = True
        app.config['DEBUG'] = True

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class ServerStatusTestCase(LiveServerTestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 5000

        return app

    def test_server_is_up_and_running(self):
        response = request.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


class UserTestCase(BaseTestCase):
    def login(self, userid, userpw):
        url = USER_URL_PREFIX + USER_LOGIN_URL
        return self.client.post(url,
                                data=dict(userid=userid,
                                          userpw=userpw))

    def logout(self):
        url = USER_URL_PREFIX + USER_LOGOUT_URL
        return self.client.get(url)

    def register(self, userid, userpw, name, email, nickname):
        url = USER_URL_PREFIX + USER_REGISTER_URL

        return self.client.post(url,
                                data=dict(userid=userid,
                                          userpw=userpw,
                                          name=name,
                                          email=email,
                                          nickname=nickname))

    def delete(self, userid, userpw):
        url = USER_URL_PREFIX + USER_REGISTER_URL
        return self.client.delete(url,
                                  data=dict(userid=userid,
                                            userpw=userpw))

    def test_userapi(self):
        userid = TEST_USERID
        userpw = TEST_USERPW
        name = TEST_USERNAME
        email = TEST_USER_EMAIL
        nickname = TEST_USER_NICKNAME

        # Need Login
        self.assert401(self.delete('asdf', 'asdf'))
        self.assert401(self.logout())

        self.assert401(self.login(userid, userpw))

        self.assert200(self.register(userid, userpw, name, email, nickname))
        self.assert200(self.register(userid * 2, userpw * 2, name * 2, email * 2, nickname * 2))

        self.assert400(self.register(userid, userpw, name, email, nickname))

        self.assert200(self.login(userid, userpw))

        # Need Logout
        self.assert401(self.login(userid, userpw))
        self.assert401(self.register(userid, userpw, name, email, nickname))

        self.assert400(self.delete('asdf', 'asdf'))

        self.assert401(self.delete(userid * 2, userpw * 2))

        self.assert200(self.delete(userid, userpw))

        self.assert200(self.logout())


class ModelingTestCase(BaseTestCase):
    @staticmethod
    def test_user_model():
        u = User(TEST_USERNAME, TEST_USERPW, TEST_USERNAME, TEST_USER_EMAIL, TEST_USER_NICKNAME)
        db.session.add(u)
        db.session.commit()

        assert u in db.session

        db.session.delete(u)
        db.session.commit()

        assert u not in db.session


if __name__ == '__main__':
    import unittest

    unittest.main()

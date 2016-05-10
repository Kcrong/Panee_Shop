# -*-coding: utf-8 -*-
from flask.ext.testing import TestCase, LiveServerTestCase

from app.models import *
from manage import app
from urllib import request
from io import BytesIO

from app.static_string import *


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['SECRET_KEY'] = 'development-test-key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

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
        url = APIS_URL_PREFIX + APIS_SESSION_URL
        return self.client.post(url,
                                data=dict(userid=userid,
                                          userpw=userpw))

    def logout(self):
        url = APIS_URL_PREFIX + APIS_SESSION_URL
        return self.client.delete(url)

    def register(self, userid, userpw, name, email, nickname):
        url = APIS_URL_PREFIX + APIS_ACCOUNT_URL

        return self.client.post(url,
                                data=dict(userid=userid,
                                          userpw=userpw,
                                          name=name,
                                          email=email,
                                          nickname=nickname))

    def current_user(self):
        url = APIS_URL_PREFIX + APIS_SESSION_URL
        return self.client.get(url)

    def user_info(self, useridnum):
        url = APIS_URL_PREFIX + APIS_ACCOUNT_URL
        return self.client.get(url,
                               data=dict(userid=useridnum))

    def delete(self, userpw):
        url = APIS_URL_PREFIX + APIS_ACCOUNT_URL
        return self.client.delete(url,
                                  data=dict(userpw=userpw))

    def upload_image(self):
        url = APIS_URL_PREFIX # + USER_IMAGE_URL
        return self.client.post(url,
                                data=dict(image=(BytesIO(b'hello World!'), 'test.txt')),
                                content_type='multipart/form-data')

    def test_userapi(self):
        userid = TEST_USERID
        userpw = TEST_USERPW
        name = TEST_USERNAME
        email = TEST_USER_EMAIL
        nickname = TEST_USER_NICKNAME
        useridnum = 1

        # Need Login
        self.assert401(self.delete('asdf'))
        self.assert401(self.logout())

        self.assert404(self.login(userid, userpw))

        self.assert200(self.register(userid, userpw, name, email, nickname))
        self.assert200(self.register(userid * 2, userpw * 2, name * 2, email * 2, nickname * 2))

        self.assert400(self.register(userid, userpw, name, email, nickname))

        self.assert200(self.login(userid, userpw))

        self.assert200(self.current_user())

        self.upload_image()

        # Need Logout
        self.assert401(self.login(userid, userpw))
        self.assert401(self.register(userid, userpw, name, email, nickname))

        self.assert401(self.delete('asdf'))

        self.assert401(self.delete(userpw * 2))

        self.assert200(self.user_info(useridnum))

        self.assert200(self.delete(userpw))

        self.assert404(self.user_info(3))


class ModelingTestCase(BaseTestCase):
    def get_or_create_user(self):
        return get_or_create(db.session, User,
                             userid=TEST_USERID,
                             userpw=TEST_USERPW,
                             name=TEST_USERNAME,
                             email=TEST_USER_EMAIL,
                             nickname=TEST_USER_NICKNAME)

    def test_user_model(self):
        u = self.get_or_create_user()

        assert u in db.session

        db.session.delete(u)
        db.session.commit()

        assert u not in db.session


if __name__ == '__main__':
    import unittest

    unittest.main()

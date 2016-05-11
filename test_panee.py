# -*-coding: utf-8 -*-
from flask.ext.testing import TestCase, LiveServerTestCase

from app.models import *
from manage import app
from urllib import request
from io import BytesIO, StringIO

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

    def upload_file(self):
        url = APIS_URL_PREFIX + APIS_FILES_URL
        return self.client.post(url,
                                data=dict(file=(BytesIO(TEST_FILEDATA), TEST_FILENAME)),
                                content_type='multipart/form-data')

    def delete_file(self, filename):
        url = APIS_URL_PREFIX + APIS_FILES_URL
        return self.client.delete(url,
                                  data=dict(filename=filename))

    def delete_image(self, filename):
        url = APIS_URL_PREFIX + APIS_FILES_URL
        return self.client.delete(url,
                                  data=dict(filename=filename))

    def upload_image(self):
        url = APIS_URL_PREFIX + APIS_FILES_URL

        with open(TEST_IMAGE, 'rb') as fp:
            test_imagedata = fp.read()

        return self.client.post(url,
                                data=dict(file=(BytesIO(test_imagedata), TEST_IMAGENAME)),
                                content_type='multipart/form-data')

    def test_api(self):
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

        # FILE UPLOAD TEST
        rep = self.upload_file()
        self.assert200(rep)

        filename = rep.json['file']

        # WRONG FILE DELETE TEST
        self.assert404(self.delete_file(filename * 2))

        # FILE DELETE TEST
        self.assert200(self.delete_file(filename))

        # Image Upload Test
        rep = self.upload_image()
        self.assert200(rep)

        # Image Delete Test
        self.assert200(self.delete_image(rep.json['file']))

        # Need Logout
        self.assert401(self.login(userid, userpw))
        self.assert401(self.register(userid, userpw, name, email, nickname))

        self.assert401(self.delete('asdf'))

        self.assert401(self.delete(userpw * 2))

        self.assert200(self.user_info(useridnum))

        self.assert200(self.delete(userpw))

        self.assert404(self.user_info(3))


class ModelingTestCase(BaseTestCase):
    """
    g_o_c means get_or_create
    """

    @staticmethod
    def g_o_c_user():
        return get_or_create(db.session, User,
                             userid=TEST_USERID,
                             userpw=TEST_USERPW,
                             name=TEST_USERNAME,
                             email=TEST_USER_EMAIL,
                             nickname=TEST_USER_NICKNAME)

    @staticmethod
    def g_o_c_shop(u):
        return get_or_create(db.session, Shop,
                             title=TEST_SHOPNAME,
                             writer=u)

    @staticmethod
    def g_o_c_comment(u, s):
        return get_or_create(db.session, Comment,
                             content=TEST_COMMENT,
                             writer=u,
                             shop=s)

    @staticmethod
    def g_o_c_score(u, s, score):
        return get_or_create(db.session, ShopScore,
                             score=score,
                             writer=u,
                             shop=s)

    @staticmethod
    def g_o_c_tag(s, name):
        return get_or_create(db.session, Tag,
                             name=name,
                             shop=s)

    @staticmethod
    def test_model():
        u = ModelingTestCase.g_o_c_user()
        s = ModelingTestCase.g_o_c_shop(u)
        c = ModelingTestCase.g_o_c_comment(u, s)
        sc1 = ModelingTestCase.g_o_c_score(u, s, TEST_FIRST_SCORE)
        sc2 = ModelingTestCase.g_o_c_score(u, s, TEST_SECOND_SCORE)
        t = ModelingTestCase.g_o_c_tag(s, TEST_TAG_NAME)

        # Check Add data
        assert u in db.session
        assert s in db.session
        assert c in db.session
        assert sc1 in db.session
        assert sc2 in db.session
        assert t in db.session

        # Check Inside data
        u = User.query.first()
        s = Shop.query.first()
        c = Comment.query.first()

        # User Check
        assert s in u.shop
        assert c in u.comment

        # Shop Check
        assert s.writer is u
        assert c in s.comment
        assert sc1 in s.all_score
        assert sc2 in s.all_score
        assert s.score == TEST_SCORE_AVERAGE
        assert t in s.tag

        # Comment Check
        assert c.writer is u
        assert c.shop is s

        # Tag Check
        assert t.shop is s


if __name__ == '__main__':
    import unittest

    unittest.main()

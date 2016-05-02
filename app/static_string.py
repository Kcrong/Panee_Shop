import os

path = os.path

from flask import jsonify

# USER URL
USER_NAME = 'user'
USER_URL_PREFIX = '/user'
USER_LOGIN_URL = '/login'
USER_LOGOUT_URL = '/logout'
USER_REGISTER_URL = '/register'

# SHOP URL
SHOP_NAME = 'shop'
SHOP_URL_PREFIX = '/shop'
SHOP_LIST_URL = '/list'

# EXPLORER URL
EXPLORER_NAME = 'explorer'
EXPLORER_URL_PREFIX = '/explorer'
EXPLORER_INDEX_URL = '/index'
EXPLORER_STATIC_URL = '/'

# EXPLORER PATH
EXPLORER_PATH = path.join(path.dirname(path.abspath(__file__)), 'api_explorer')
EXPLORER_STATIC_PATH = path.join(EXPLORER_PATH, 'static')
EXPLORER_TEMPLATE_PATH = path.join(EXPLORER_PATH, 'templates')

# FOR TESTCASE
TEST_USERID = 'test'
TEST_USERPW = 'test'
TEST_USERNAME = '이름'
TEST_USER_EMAIL = 'email@email.com'
TEST_USER_NICKNAME = 'testnick'


def json_message(message="Success", code=200):
    response = jsonify({'message': message,
                        'status': code})
    response.status_code = code
    return response

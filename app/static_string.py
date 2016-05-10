import os

path = os.path

from flask import jsonify

APP_PATH = path.dirname(path.abspath(__file__))
UPLOAD_PATH = path.join(APP_PATH, 'uploads')

# APIS URL
APIS_NAME = 'apis'
APIS_URL_PREFIX = '/apis'
APIS_ACCOUNT_URL = '/account'
APIS_SESSION_URL = '/session'
APIS_ACCOUNT_GETS_URL = '/accounts'

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
EXPLORER_PATH = path.join(APP_PATH, 'api_explorer')
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

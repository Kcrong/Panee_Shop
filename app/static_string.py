import os

path = os.path

from flask import jsonify
from config import PROJECT_PATH

APP_PATH = path.dirname(path.abspath(__file__))
UPLOAD_PATH = path.join(APP_PATH, 'uploads')

SMALL_IMAGE_SIZE = 0.3
SMALL_IMAGE_NAME_HEADER = 'small_'
MEDIUM_IMAGE_SIZE = 0.7
MEDIUM_IMAGE_NAME_HEADER = 'medium_'

# APIS URL
APIS_NAME = 'apis'
APIS_URL_PREFIX = '/apis'
APIS_ACCOUNT_URL = '/account'
APIS_SESSION_URL = '/session'
APIS_ACCOUNT_GETS_URL = '/accounts'
APIS_FILES_URL = '/file'

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
TEST_FILENAME = 'test.txt'
TEST_FILEDATA = b'this is test file~!~!~!~!'
TEST_IMAGENAME = 'test.png'
TEST_IMAGE = os.path.join(PROJECT_PATH, 'tests', 'image.png')


def json_message(message="Success", code=200, **kwargs):

    kwargs.update({'message': message,
                   'status': code})

    response = jsonify(kwargs)

    response.status_code = code
    return response

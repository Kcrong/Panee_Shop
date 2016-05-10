import os
import random
import string

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

try:
    DEBUG = os.environ['FLASK_DEBUG'] == 'true'
except KeyError:
    DEBUG = True


def randomkey(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


if DEBUG:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_PATH, 'testdb.db')
    SECRET_KEY = 'development-key'
else:
    SQLALCHEMY_DATABASE_URI = 'mysql://panee:panee123@localhost:3306/panee?charset=utf8'
    SECRET_KEY = randomkey(30)

STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'client')
USE_METHOD = ['GET', 'POST', 'PUT', 'DELETE']

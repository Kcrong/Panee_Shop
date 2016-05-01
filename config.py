import os

try:
    DEBUG = os.environ['FLASK_DEBUG'] == 'true'
except KeyError:
    DEBUG = False

if DEBUG:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/testdb.db'
else:
    SQLALCHEMY_DATABASE_URI = 'mysql://panee:panee123@localhost:3306/panee?charset=utf8'
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'client')
USE_METHOD = ['GET', 'POST', 'PUT', 'DELETE']
SECRET_KEY = 'development-key'

import random
import string


def randomkey(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


HOST = '0.0.0.0'
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql://panee:panee123@localhost:3306/panee?charset=utf8'
SECRET_KEY = randomkey(30)
SQLALCHEMY_POOL_RECYCLE = 3600
FACEBOOK_APP_SECRET = 'c89b148848fa64814023db3765865ef0'
FACEBOOK_APP_ID = '598620056957375'

import os.path

DEBUG = True
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'client')
USE_METHOD = ['GET', 'POST', 'PUT', 'DELETE']
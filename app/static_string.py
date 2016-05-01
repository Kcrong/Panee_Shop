import os
path = os.path

# USER URL
USER_NAME = 'user'
USER_URL_PREFIX = '/user'
USER_LOGIN_URL = '/login'
USER_LOGOUT_URL = '/logout'

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


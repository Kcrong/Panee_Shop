from flask_restful import reqparse

import config
from app.static_string import *
from . import api

api_parser = {
    resource[1][0]: {method: reqparse.RequestParser() for method in config.USE_METHOD}
    for resource in api.resources
    }

# USER_MAIN - GET : 현재 사용자 정보
parser = api_parser[APIS_ACCOUNT_URL]['GET']
parser.add_argument('userid', type=int, help='Need User ID number', required=True)

# USER_MAIN - POST: 사용자 등록 (회원가입)
parser = api_parser[APIS_ACCOUNT_URL]['POST']
parser.add_argument('userid', type=str, help='Need String Userid', required=True)
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)
parser.add_argument('name', type=str, help='Need String name', required=True)
parser.add_argument('email', type=str, help='Need String email', required=True)
parser.add_argument('nickname', type=str, help='Need String nickname', required=True)

# USER_MAIN - PUT: 사용자 정보 변경
parser = api_parser[APIS_ACCOUNT_URL]['PUT']
parser.add_argument('userid', type=str, help='Need String Userid to change', required=True)
parser.add_argument('userpw', type=str, help='Need String Userpw to change', required=True)
parser.add_argument('name', type=str, help='Need String name to change', required=True)
parser.add_argument('email', type=str, help='Need String email to change', required=True)
parser.add_argument('nickname', type=str, help='Need String nickname to change', required=True)

# USER_MAIN - GETS: 회원들 정보??
" Can't understand"

# USER_MAIN - DELETE: 회원탈퇴
parser = api_parser[APIS_ACCOUNT_URL]['DELETE']
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)

# USER_SESSION - GET: 접속중인 사용자
"NO required args"

# USER_SESSION - POST: 로그인
parser = api_parser[APIS_SESSION_URL]['POST']
parser.add_argument('userid', type=str, help='Need String Userid', required=True)
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)

# USER_SESSION - DELETE: 로그아웃
"NO required args"


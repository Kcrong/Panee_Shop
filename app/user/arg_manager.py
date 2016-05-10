from flask_restful import reqparse

import config
from app.static_string import USER_MAIN_URL, USER_SESSION_URL, USER_IMAGE_URL
from .views import user_api

user_parser = {
    resource[1][0]: {method: reqparse.RequestParser() for method in config.USE_METHOD}
    for resource in user_api.resources
    }

# USER_MAIN - GET : 현재 사용자 정보
parser = user_parser[USER_MAIN_URL]['GET']
parser.add_argument('userid', type=int, help='Need User ID number', required=True)

# USER_MAIN - POST: 사용자 등록 (회원가입)
parser = user_parser[USER_MAIN_URL]['POST']
parser.add_argument('userid', type=str, help='Need String Userid', required=True)
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)
parser.add_argument('name', type=str, help='Need String name', required=True)
parser.add_argument('email', type=str, help='Need String email', required=True)
parser.add_argument('nickname', type=str, help='Need String nickname', required=True)

# USER_MAIN - GETS: 회원들 정보??
" Can't understand"

# USER_MAIN - DELETE: 회원탈퇴
parser = user_parser[USER_MAIN_URL]['DELETE']
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)

# USER_SESSION - GET: 접속중인 사용자
"NO required args"

# USER_SESSION - POST: 로그인
parser = user_parser[USER_SESSION_URL]['POST']
parser.add_argument('userid', type=str, help='Need String Userid', required=True)
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)

# USER_SESSION - DELETE: 로그아웃
"NO required args"

# USER_IMAGE - GET: 유저 이미지 가져오기
parser = user_parser[USER_IMAGE_URL]['GET']
parser.add_argument('userid', type=str, help='Need String Userid', required=True)

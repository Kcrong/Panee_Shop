from flask_restful import reqparse
from werkzeug.datastructures import FileStorage

import config
from app.static_string import *
from .views import main_api

apis_parser = {
    resource[1][0]: {method: reqparse.RequestParser() for method in config.USE_METHOD}
    for resource in main_api.resources
    }

# USER_MAIN - GET : 현재 사용자 정보
parser = apis_parser[APIS_ACCOUNT_URL]['GET']
parser.add_argument('userid', type=int, help='Need User ID number', required=True)

# USER_MAIN - POST: 사용자 등록 (회원가입)
parser = apis_parser[APIS_ACCOUNT_URL]['POST']
parser.add_argument('userid', type=str, help='Need String Userid', required=True)
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)
parser.add_argument('name', type=str, help='Need String name', required=True)
parser.add_argument('email', type=str, help='Need String email', required=True)
parser.add_argument('nickname', type=str, help='Need String nickname', required=True)

# USER_MAIN - GETS: 회원들 정보??
" Can't understand"

# USER_MAIN - DELETE: 회원탈퇴
parser = apis_parser[APIS_ACCOUNT_URL]['DELETE']
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)

# USER_SESSION - GET: 접속중인 사용자
"NO required args"

# USER_SESSION - POST: 로그인
parser = apis_parser[APIS_SESSION_URL]['POST']
parser.add_argument('userid', type=str, help='Need String Userid', required=True)
parser.add_argument('userpw', type=str, help='Need String Userpw', required=True)

# USER_SESSION - DELETE: 로그아웃
"NO required args"

# USER_IMAGE - POST: 파일 추가
parser = apis_parser[APIS_FILES_URL]['POST']
parser.add_argument('file', type=FileStorage, location='files', help='Need file to upload', required=True)

# USER_IMAGE - DELETE: 파일 삭제
parser = apis_parser[APIS_FILES_URL]['DELETE']
parser.add_argument('filename', type=str, help='Need filename to delete (After randomize)', required=True)
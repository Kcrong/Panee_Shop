import config
from . import file_api
from app.static_string import *
from werkzeug.datastructures import FileStorage
from flask_restful import reqparse

file_api_parser = {
    resource[1][0]: {method: reqparse.RequestParser() for method in config.USE_METHOD}
    for resource in file_api.resources
}

# USER_IMAGE - POST: 파일 추가
parser = file_api_parser[APIS_FILES_URL]['POST']
parser.add_argument('file', type=FileStorage, location='files', help='Need file to upload', required=True)

# USER_IMAGE - DELETE: 파일 삭제
parser = file_api_parser[APIS_FILES_URL]['DELETE']
parser.add_argument('filename', type=str, help='Need filename to delete (After randomize)', required=True)
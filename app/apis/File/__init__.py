from flask import Blueprint
from flask_restful import Api
from app.static_string import *

file_api = Api()
file_blueprint = Blueprint(FILE_API_NAME, __name__)

file_api.init_app(file_blueprint)

from .view import *


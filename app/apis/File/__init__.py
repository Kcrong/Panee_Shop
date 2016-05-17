from flask import Blueprint
from flask_restful import Api
from app.static_string import *

api = Api()
blueprint = Blueprint(FILE_API_NAME, __name__)

api.init_app(blueprint)

from .view import *


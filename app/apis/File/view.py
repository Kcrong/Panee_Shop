from flask import request
from app.static_string import *
from app import RestBase
from . import file_api
from app.models import *


@file_api.resource(APIS_FILES_URL)
class File(RestBase):
    def __init__(self):
        self.parser = file_api_parser[APIS_FILES_URL][request.method]

    def post(self):
        file = self.args['file']

        f = Files(file)

        db.session.add(f)
        db.session.commit()

        return json_message(file=f.random)

    def delete(self):
        filename = self.args['filename']

        f = Files.query.filter_by(random=filename).first_or_404()

        f.delete()

        db.session.commit()

        return json_message()


from .arg_manager import file_api_parser

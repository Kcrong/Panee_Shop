from app.static_string import *
from flask import request
from app import RestBase
from . import user_api
from ..login_manager import *
from app.models import *
from sqlalchemy.exc import IntegrityError


@user_api.resource(APIS_ACCOUNT_URL)
class Main(RestBase):
    def __init__(self):
        self.parser = user_api_parser[APIS_ACCOUNT_URL][request.method]

    def get(self):
        args = self.args
        u = Users.query.filter_by(id=args['userid'], is_active=True).first_or_404()
        return jsonify(u.base_info_dict)

    @login_required
    def delete(self):
        u = current_user()
        if u.userpw != self.args['userpw']:
            return json_message('Diff password', 401)
        else:
            u.active = False
            db.session.commit()
            logout_user()
            return json_message()

    @logout_required
    def post(self):
        args = self.args
        u = Users(args['userid'], args['userpw'], args['name'], args['email'], args['nickname'])

        db.session.add(u)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()

            message = "%s is duplicate" % e.args[0].split(':')[1].split('.')[1]

            return json_message(message, 400)

        else:
            return json_message()

    @login_required
    def put(self):
        args = self.args
        u = Users.query.filter_by(userid=args['userid'], active=True).first_or_404()
        u.userpw = args['userpw']
        u.name = args['name']
        u.email = args['email']
        u.nickname = args['nickname']

        db.session.commit()

        return json_message()


@user_api.resource(APIS_SESSION_URL)
class Session(RestBase):
    def __init__(self):
        self.parser = user_api_parser[APIS_SESSION_URL][request.method]

    @login_required
    def get(self):
        u = current_user()
        return jsonify(u.base_info_dict)

    @logout_required
    def post(self):
        args = self.args
        u = Users.query.filter_by(userid=args['userid'], userpw=args['userpw'], is_active=True).first_or_404()
        login_user(u.userid)
        return json_message()

    @login_required
    def delete(self):
        logout_user()
        return json_message()


from .arg_manager import user_api_parser

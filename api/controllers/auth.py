from flask_restful import reqparse, abort, Resource
from api.models import User
from api.utils.errors import ValidationError

class AuthLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help="enter your email", required=True)
        parser.add_argument('password', type=str, help="enter your password", required=True)

        args = parser.parse_args()

        email = args.get('email')
        password = args.get('password')

        try:
            token = User.validate(email, password)
            return {'token': token}
        except ValidationError as e:
            abort(400, message='error logging in ->{}'.format(str(e)))


class AuthRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fullname', type=str, help="enter your fullname", required=True)
        parser.add_argument('email', type=str, help="enter your email", required=True)
        parser.add_argument('password', type=str, help="enter a password", required=True)
        parser.add_argument('password_conf', type=str, help="enter password confirmation", required=True)

        args = parser.parse_args()

        email = args.get('email')
        password = args.get('password')
        password_conf = args.get('password_conf')
        fullname = args.get('fullname')

        try:
            User.create(
                email=email,
                password=password,
                password_conf=password_conf,
                fullname=fullname
            )
            return {'message': 'Successfully created your account.'}
        except ValidationError as e:
            abort(400, message='Error creating account -> {}'.format(str(e)))

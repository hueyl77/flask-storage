from jose import jwt
from jose.exceptions import JWTError
from functools import wraps

from flask import current_app, request, g
from flask_restful import abort

from api.models import User, File

def login_required(f):
    @wraps(f)
    def func(*args, **kwargs):
        try:
            if 'authorization' not in request.headers:
                abort(404, message="Not logged in")
            token = request.headers.get('authorization')
            payload = jwt.decode(token, current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
            user_id = payload['id']
            g.user = User.find(user_id)
            if g.user is None:
                abort(404, message="The user id is invalid")
            return f(*args, **kwargs)
        except JWTError as e:
            abort(400, message="Error parsing token ->{}".format(str(e)))

    return func


def validate_user(f):
    @wraps(f)
    def func(*args, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id != g.user['id']:
            abort(404, message="No permission to resource")
        return f(*args, **kwargs)

    return func


def belongs_to_user(f):
    @wraps(f)
    def func(*args, **kwargs):
        file_id = kwargs.get('file_id')
        user_id = kwargs.get('user_id')
        file = File.find(file_id, True)

        if not file or file['creator'] != user_id:
            abort(404, message="File not found")

        g.file = file
        return f(*args, **kwargs)

    return func


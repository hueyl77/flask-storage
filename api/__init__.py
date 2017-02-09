from flask import Flask, Blueprint
from flask_restful import Api

from api.controllers import auth, files
from config import config

def create_app(env):
    app = Flask(__name__)
    app.config.from_object(config[env])

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    api.add_resource(auth.AuthLogin, '/auth/login')
    api.add_resource(auth.AuthRegister, '/auth/register')
    api.add_resource(files.CreateList, '/users/<string:user_id>/files')
    api.add_resource(files.ViewEditDelete, '/users/<string:user_id>/files/<string:file_id>')

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app

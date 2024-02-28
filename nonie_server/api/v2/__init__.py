'''
API v2 resources
'''
from flask_restful import Api
from flask import Blueprint
from nonie_server.api.v2.resources import hello

bp = Blueprint('v2', __name__)

api = Api(bp)
api.add_resource(hello.HelloWorld, '/api/v2/hello')

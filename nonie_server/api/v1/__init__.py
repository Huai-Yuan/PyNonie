'''
API v2 resources
'''
from flask import Blueprint, session, g
from flask_restful import Api
from nonie_server.db import get_db
from nonie_server.api.v1.resources import hello, user, blog


bp = Blueprint('v1', __name__)

api = Api(bp)
api.add_resource(hello.HelloWorld, '/api/v1/hello')
api.add_resource(user.Register, '/api/v1/user/register')
api.add_resource(user.Login, '/api/v1/user/login')
api.add_resource(user.Logout, '/api/v1/user/logout')
api.add_resource(blog.Create, '/api/v1/blog/create')
api.add_resource(blog.Blog, '/api/v1/blog/<string:post_id>')

@bp.before_app_request
def load_logged_in_user():
    '''
    Load the currently logged-in user from the session.

    If the user is logged in, the `g.user` global variable will be set to the user's information.
    If the user is not logged in, `g.user` will be set to None.
    '''
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

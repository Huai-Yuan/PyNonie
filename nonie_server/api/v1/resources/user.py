'''
API Resource for user manipulations
'''
import functools
from flask import request, session, g
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash
from nonie_server.db import get_db


class Register(Resource):
    '''
    This class handles the registration of new users.

    Attributes:
    - post: A method that handles POST requests to register a new user.
    '''
    def post(self):
        '''
        Handles the POST request to register a new user.

        Returns:
        - dict: A JSON response containing a message indicating success or an error message.
        '''
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f'User {username} is already registered.'
            else:
                return {'message': 'Registered successfully!'}

        return {'message': error}


class Login(Resource):
    '''
    A class to handle the login functionality.

    Attributes:
        None.

    Methods:
        post(self): Method to handle the POST request for login.
    '''
    def post(self):
        '''
        Handles the POST request for user login.

        Returns:
            dict: A dictionary containing a message indicating the status of the login attempt.
        '''
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return {'message': f'Hi, {username}'}

        return {'message': error}


class Logout(Resource):
    '''
    A class to handle the logout functionality.

    Attributes:
        None.

    Methods:
        get(self): Method to handle the GET request for logout.
    '''
    def get(self):
        '''
        Handle the GET request for logout.

        Returns:
            dict: A dictionary containing a message indicating successful logout.
        '''
        session.clear()
        return {'message': 'Logout successfully!'}


def login_required(view):
    '''
    A decorator that redirects users to the login page if they are not logged in.

    Parameters:
        view: The view function to be wrapped.

    Returns:
        The wrapped view function.
    '''
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return {'message': 'Login required!'}
        return view(*args, **kwargs)

    return wrapped_view

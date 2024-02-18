'''
authentication functions
'''
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from pynonie.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    '''
    Register a new user.

    Returns:
        A redirect to the login page if registration is successful, otherwise renders the registration page.
    '''
    if request.method == 'POST':
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
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    '''
    Handle user login.

    Returns:
        The rendered login page if the request method is GET or if
        the login was unsuccessful. Otherwise, a redirect to the index page.
    '''
    if request.method == 'POST':
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
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


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


@bp.route('/logout')
def logout():
    '''
    Logout function that clears the session and redirects to the index page.

    Returns:
        A redirect to the index page.
    '''
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    '''
    A decorator that redirects users to the login page if they are not logged in.

    Parameters:
        view: The view function to be wrapped.

    Returns:
        The wrapped view function.
    '''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

import pytest
from flask import Flask, g, session
from flask.testing import FlaskClient
from nonie_server.db import get_db 


def test_register(client: FlaskClient, app: Flask):
    response = client.post(
        '/api/v1/user/register',
        data={'username': 'a', 'password': 'a'}
    )
    assert b'Registered successfully!' in response.data

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(
    client: FlaskClient, username, password, message
):
    response = client.post(
        '/api/v1/user/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client: FlaskClient, auth):
    auth.login()

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session

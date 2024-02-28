import pytest
from flask import Flask
from flask.testing import FlaskClient
from nonie_server.db import get_db


@pytest.mark.parametrize(('path', 'method'), (
    ('/api/v1/blog/create', 'post'),
    ('/api/v1/blog/1', 'put'),
    ('/api/v1/blog/1', 'delete'),
))
def test_login_required(client: FlaskClient, path, method):
    if method == 'post':
        response = client.post(path)
    elif method == 'get':
        response = client.get(path)
    elif method == 'put':
        response = client.put(path)
    elif method == 'delete':
        response = client.delete(path)
    assert b'Login required!' in response.data


def test_author_required(app: Flask, client: FlaskClient, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.put('/api/v1/blog/1').status_code == 403
    assert client.delete('/api/v1/blog/1').status_code == 403


@pytest.mark.parametrize(('path', 'method'), (
    ('/api/v1/blog/2', 'put'),
    ('/api/v1/blog/2', 'delete'),
))
def test_exists_required(client: FlaskClient, auth, path, method):
    auth.login()
    if method == 'put':
        response = client.put(path)
    elif method == 'delete':
        response = client.delete(path)
    assert response.status_code == 404


def test_create(client: FlaskClient, auth, app):
    auth.login()
    client.post('/api/v1/blog/create', data={'title': 'created', 'body': ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2


def test_update(client: FlaskClient, auth, app):
    auth.login()
    client.put('/api/v1/blog/1', data={'title': 'updated', 'body': ''})

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'


@pytest.mark.parametrize(('path', 'method'), (
    ('/api/v1/blog/create', 'post'),
    ('/api/v1/blog/1', 'put'),
))
def test_create_update_validate(client: FlaskClient, auth, path, method):
    auth.login()
    if method == 'post':
        response = client.post(path, data={'title': '', 'body': ''})
    elif method == 'put':
        response = client.put(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


def test_delete(client: FlaskClient, auth, app):
    auth.login()
    client.delete('/api/v1/blog/1')
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None

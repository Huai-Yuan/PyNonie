from nonie_server import create_app
from flask.testing import FlaskClient


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello_v1(client: FlaskClient):
    response = client.get('/api/v1/hello')
    assert response.json['message'] == 'Hello, World! v1'


def test_hello_v2(client: FlaskClient):
    response = client.get('/api/v2/hello')
    assert response.json['message'] == 'Hello, World! v2'

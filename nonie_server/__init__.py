'''
flask app
'''
import os
from flask import Flask
from nonie_server.api import v1, v2
from nonie_server import db


def create_app(test_config=None) -> Flask:
    '''
    Create and configure the Flask app.

    Parameters:
        test_config (dict, optional): The test configuration. Defaults to None.

    Returns:
        flask.Flask: The configured Flask app.
    '''
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'NonieServer.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(v1.bp)
    app.register_blueprint(v2.bp)

    return app

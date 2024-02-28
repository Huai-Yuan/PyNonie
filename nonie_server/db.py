'''
database manipulation
'''
import sqlite3
import click
from flask import Flask
from flask import current_app, g


def get_db():
    '''
    Connect to the application's configured database.
    
    Returns:
        A connection to the database.
    '''
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(_=None):
    '''
    Close the database connection.

    Parameters:
        exception: An optional exception that may have occurred.
    '''
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    '''
    Initialize the database by executing the schema.sql file.
    '''
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    '''Clear the existing data and create new tables.'''
    init_db()
    click.echo('Initialized the database.')


def init_app(app: Flask):
    '''
    Register database functions with the Flask app. This is called by the application factory.

    Parameters:
        app: The Flask app instance.
    '''
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

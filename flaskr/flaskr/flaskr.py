# imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from contextlib import closing

app = Flask(__name__)  # create our little application :)
app.config.from_object(__name__)  # load config from this file

# Load default config and override config from an env var
app.config.from_object(obj=dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar(variable_name='FLASKR_SETTINGS', silent=False)


# used to open a connection on request
def connect_db():
    """Connects to the specific database"""
    rv = sqlite3.connect(database=app.config['DATABASE'])
    rv.row_factory = sqlite3.Row  # represent rows as dictionaries not tuples
    return rv


def init_db():
    """Creates the database per 'schema.sql' script."""
    db = get_db()
    with app.open_resource(resource='schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


# register a new command with the flask script
@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the current
    application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


# close db when application context tears down
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# fires up the server if we want to run as standalone app
if __name__ == '__main__':
    app.run()

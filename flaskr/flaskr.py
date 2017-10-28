# imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from contextlib import closing

# TODO - refactor into configuration file
# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


# used to open a connection on request
def connect_db():
    return sqlite3.connect(database=app.config['DATABASE'])


# initializes the database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(resource='schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# connect to db before request
@app.before_request
def before_request():
    g.db = connect_db()


# close db post request
@app.teardown_request
def teardown_request(exception):
    db = getattr(o=g, name='db', default=None)
    if db is not None:
        db.close()


# fires up the server if we want to run as standalone app
if __name__ == '__main__':
    app.run()

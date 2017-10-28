# imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

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


# fires up the server if we want to run as standalone app
if __name__ == '__main__':
    app.run()

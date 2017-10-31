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

#############################
# Database Management Functions
#############################

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


#############################
# View Functions
#############################

# Show Entries View
@app.route(rule='/')
def show_entries():
    """This view shows all the entries stored in the database."""
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template(template_name_or_list='show_entries.html',
                           entries=entries)


# Add New Entry View
@app.route(rule='/add', methods=['POST'])
def add_entry():
    """This view lets user add new entries if they are logged in. This only
    responds to 'POST' requests; the actual form is sown on the show_entries
    pages.

    If everything worked out well, it will 'flash()' an information
    message to the next request and redirect back to the 'show_entries' page."""
    if not session.get('logged_in'):
        abort(status=401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash(message='New entry was successfully posted')
    return redirect(location=url_for(endpoint='show_entries'))


# Login and Logout Views
@app.route(rule='/login', methods=['GET', 'POST'])
def login():
    """Checks the username and password against the ones from the
    configuration and sets the 'logged_in' key for the session.

    If the user logged in successfully, that key is set to 'True', and the
    user is redirected back to the 'show_entries' page.

    In addition, a message is flashed that informs the user that he or she
    was logged in successfully. If an error occurred, the template is notified
    about that, and the user is asked again."""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash(message='You were logged in')
            return redirect(location=url_for(endpoint='show_entries'))
    return render_template(template_name_or_list='login.html', error=error)


@app.route(rule='/logout')
def logout():
    """On logout, removes the 'logged_in' key from the session."""
    session.pop('logged_in', None)  # do nothing if no key
    flash(message='You were logged out')
    return redirect(location=url_for(endpoint='show_entries'))


# fires up the server if we want to run as standalone app
if __name__ == '__main__':
    app.run()

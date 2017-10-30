# imports
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)


#############################
# View Functions
#############################

@app.route('/')
def show_about():
    page_title = 'John Kwening'
    return render_template(template_name_or_list='about.html',
                           page_title=page_title)


@app.route('/projects')
def show_projects():
    page_title = 'John\'s Projects'
    return render_template(template_name_or_list='projects.html',
                           page_title=page_title)


@app.route('/resume')
def show_resume():
    page_title = 'John\'s Resume'
    return render_template(template_name_or_list='projects.html',
                           page_title=page_title)


@app.route('/activity_tracker')
def show_activities():
    page_title = 'John\'s Activities'
    return render_template(template_name_or_list='activity_tracker.html',
                           page_title=page_title)


if __name__ == '__main__':
    app.run()

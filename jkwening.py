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
    return render_template(template_name_or_list='about.html')


# bind other urls to show_about view function
app.add_url_rule(rule='/about', endpoint='about', view_func=show_about)


@app.route('/projects')
def show_projects():
    return render_template(template_name_or_list='projects.html')


@app.route('/resume')
def show_resume():
    return render_template(template_name_or_list='resume.html')


@app.route('/activity_tracker')
def show_activities():
    return render_template(template_name_or_list='activity_tracker.html')


if __name__ == '__main__':
    app.run()

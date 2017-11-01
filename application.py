# imports
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

application = Flask(__name__)


#############################
# View Functions
#############################

@application.route('/')
def show_about():
    return render_template(template_name_or_list='about.html')


# bind other urls to show_about view function
application.add_url_rule(rule='/about', endpoint='about', view_func=show_about)


@application.route('/projects')
def show_projects():
    return render_template(template_name_or_list='projects.html')


@application.route('/resume')
def show_resume():
    return render_template(template_name_or_list='resume.html')


@application.route('/activity_tracker')
def show_activities():
    return render_template(template_name_or_list='activity_tracker.html')


if __name__ == '__main__':
    application.run()

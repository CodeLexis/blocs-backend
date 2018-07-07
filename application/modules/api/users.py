"""Developers' relationships are fostered by
    1. Location
    2. Programming Languages
    3. Software Sector"""
from application.modules.api import api_blueprint


@api_blueprint.route('/users/<user_uid>')
def show_user_metadata():
    pass


@api_blueprint.route('/users/<user_uid>/conversations')
def show_user_conversations():
    pass


@api_blueprint.route('/users/<user_uid>/projects')
def show_user_projects():
    pass


@api_blueprint.route('/users/<user_uid>/events')
def show_user_events():
    {'interested': [], 'created': [], 'invited': []}
    pass


@api_blueprint.route('/users/<user_uid>/articles')
def show_user_articles():
    pass

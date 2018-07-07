from flask import Blueprint


web_blueprint = Blueprint('web_blueprint', __name__, url_prefix='')


@web_blueprint.route('/')
def render_hi():
    return 'Welcome to Blocs!'


@web_blueprint.route('/privacy')
def render_privacy_policy():
    return 'Your data is private. I tell you...'

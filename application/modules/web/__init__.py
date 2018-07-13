from flask import Blueprint, Response
from flask import render_template, request


web_blueprint = Blueprint('web_blueprint', __name__, url_prefix='')


from .blocs import *
from .courses import *
from .events import *
from .jobs import *


@web_blueprint.route('/')
def render_hi():
    return 'Welcome to Blocs!'


@web_blueprint.route('/privacy')
def render_privacy_policy():
    return 'Your data is private. I tell you...'


@web_blueprint.route('/avatars/default/<color>')
def render_default_avatar(color):
    default_avatar = open(
        'static/assets/default_avatars/{}.png'.format(color), 'rb').read()

    return Response(default_avatar, mimetype='image')

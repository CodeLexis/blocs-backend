from flask import Blueprint


web_blueprint = Blueprint('web_blueprint', __name__, url_prefix='')


@web_blueprint.route('/')
def render_hi():
    return 'Welcome to Blocs!'

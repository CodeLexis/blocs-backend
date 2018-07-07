from flask import Blueprint


web = Blueprint('web', __name__)


@web.route('')
def render_hi():
    return

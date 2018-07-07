from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from application.core import setup_core_tools
# from application.core.utils.contexts.handlers import after_every_request
# from application.core.utils.contexts.handlers import before_every_request
from config import load_configuration


def _bind_request_contexts_handlers(app, blueprint):
    # Bind before and after request context handlers to blueprint

    app.before_request_funcs.setdefault(
        blueprint.name, []).insert(0, before_every_request)
    app.after_request_funcs.setdefault(
        blueprint.name, []).insert(0, after_every_request)


def _setup_blueprints(app):
    from application.modules.api import api_blueprint
    from application.modules.bots import bots_blueprint
    from application.modules.web import web_blueprint

    app.register_blueprint(api_blueprint)
    app.register_blueprint(bots_blueprint)
    app.register_blueprint(web_blueprint)

    # _bind_request_contexts_handlers(app, api_blueprint)


def create_app(config_mode):
    """Create a Flask application instance."""

    # Create application instance;
    # Get the configuration settings
    # for instance and update it
    app = Flask(__name__, instance_relative_config=True)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    load_configuration(app, config_mode)
    setup_core_tools(app)
    # celery = make_celery(app)
    _setup_blueprints(app)

    return app

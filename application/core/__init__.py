from random import SystemRandom

from flask_sqlalchemy import SQLAlchemy

from application.core.logs import logger, setup_logging


rand_gen = SystemRandom()
db = SQLAlchemy()


def setup_core_tools(app):
    from application.core.errors.handlers import setup_error_handling

    setup_logging(app)

    setup_error_handling(app)

    db.init_app(app)

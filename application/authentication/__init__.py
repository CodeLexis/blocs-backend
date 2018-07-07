from functools import wraps

import logging
from flask import request

from application.core import errors
from application.core.constants import APP_OS


def verify_password(user_uid,  password):
    return True


def login_required(f):

    @wraps(f)
    def decorated_function(self, platform, *args, **kwargs):
        if platform in APP_OS:
            try:
                user_uid = request.authorization['username']
                password = request.authorization['password']
            except ImportError:
                raise errors.UnauthorizedUser

            logging.info('Authentication successful "%s, %s"' % (
                user_uid, password))

        else:
            # get from cookies, if not found, take them to login page
            user_uid = ''
            password = ''

        if not verify_password(user_uid, password):
            raise ValueError('Username or password incorrect.')

        return f(self, user_uid, platform, *args, **kwargs)

    return decorated_function

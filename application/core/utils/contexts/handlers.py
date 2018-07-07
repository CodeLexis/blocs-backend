import json
from functools import wraps

from flask import g, request

from application.core import errors
from application.core.constants import SUPPORTED_HTTP_METHODS
from application.core.utils.contexts import (current_api_log,
                                             current_api_log_id,
                                             current_request_headers,
                                             current_user_id)


def _update_api_log(api_log_id, request_method, request_url, user_id,
                    response_data=None, request_headers=None):
    """Update the API log on completing request handling."""
    # from application.core.models import APILog

    endpoint = (
        '{HTTP_METHOD} {ENDPOINT}'.format(
            HTTP_METHOD=request_method,
            ENDPOINT=request_url
        )
    )

    # api_log = APILog.query.get(api_log_id)
    api_log = current_api_log()  # Stub until task queue (Celery) is added
    # if api_log is None:
    #     logger.error('API activity is None. yourResponse: '
    #                  '{0}'.format(repr(response_data)))
    #     return False

    try:
        response_data = json.dumps(response_data)
    except:
        pass

    api_log.update(
        created_by=user_id,
        request_headers=json.dumps(request_headers),
        response_data=response_data,
        endpoint=endpoint,
        error_msg='API activity logging update failed!')

    # return True


def before_every_request():
    """Do some necessary setup before handling any request."""

    try:
        # DB-persist new API activity
        g.api_log = current_api_log()
    except:
        raise errors.APIError(
            log_message='Error persisting API activity to DB!')


# def do_cors_support(response):
#     allowed_methods = ', '.join(SUPPORTED_HTTP_METHODS)
#
#     response.headers['Access-Control-Allow-Origin'] = (
#         request.headers.get('Origin', '*')
#     )
#     response.headers['Access-Control-Allow-Credentials'] = 'true'
#     response.headers['Access-Control-Allow-Methods'] = allowed_methods
#     response.headers['Access-Control-Request-Headers'] = (
#         request.headers.get('Access-Control-Request-Headers',
#                             'Authorization')
#     )
#
#     # if current_app.debug:
#     #     # control client caching age
#     #     response.headers['Access-Control-Max-Age'] = 1


def add_cors_support(f):
    allowed_methods = ', '.join(SUPPORTED_HTTP_METHODS)

    @wraps(f)
    def decorated_func(*args, **kwargs):
        response = f(*args, **kwargs)

        response.headers['Access-Control-Allow-Origin'] = (
            request.headers.get('Origin', '*')
        )
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = allowed_methods
        response.headers['Access-Control-Allow-Headers'] = (
            request.headers.get('Access-Control-Request-Headers',
                                'Authorization')
        )

        return response

    return decorated_func


@add_cors_support
def after_every_request(response):
    """Do necessary operations after every request."""
    # Update API activity log: Save response payload

    try:
        response_data = response.response[0]
    except IndexError:
        response_data = None

    _update_api_log(
        api_log_id=current_api_log_id(),
        request_method=request.method,
        request_url=request.url,
        user_id=current_user_id(),
        response_data=response_data,
        request_headers=current_request_headers())

    return response

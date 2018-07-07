from datetime import datetime

from flask import g, request

from application.core import errors, logger
from application.core.constants import (PAYLOADABLE_HTTP_METHODS,
                                        SUPPORTED_HTTP_METHODS)
from application.core.utils.helpers import generate_unique_reference
from application.core.utils.normalizers import normalize_request_data

# from tasks import task_update_api_activity


def current_request_time():
    try:
        return g.current_request_time
    except AttributeError:
        g.current_request_time = datetime.now()
        return g.current_request_time


def current_user():
    try:
        return g.user
    except AttributeError:
        return None


def current_user_id():
    try:
        return g.user.id
    except AttributeError:
        return None


def current_api_log():
    try:
        return g.api_log
    except AttributeError:
        from application.core.models.helpers import create_api_log
        g.api_log = create_api_log()
        return g.api_log


def current_api_log_id():
    try:
        return g.api_log.id
    except AttributeError:
        return None


def current_api_ref():
    try:
        return g.api_ref
    except AttributeError:
        g.api_ref = generate_unique_reference()
        return g.api_ref


def current_request_ip():
    try:
        return g.request_ip
    except AttributeError:
        g.request_ip = (
            request.access_route[-1]
            or request.environ.get('HTTP_X_REAL_IP',
                                   request.remote_addr)
        )
        return g.request_ip


def current_request_data(force=True, silent=True, cache=True):
    try:
        return g.request_data
    except AttributeError:
        g.request_data = None

        if request.method not in SUPPORTED_HTTP_METHODS:
            logger.error('Received request with an unsupported '
                         'HTTP method: {0}'.format(request.method))
            raise errors.HTTPRequestMethodNotSupported()

        if request.method in PAYLOADABLE_HTTP_METHODS:
            # Get the data sent with the request: JSON or plain
            # text data and parse it into a Python dictionary-type data
            try:
                g.request_data = normalize_request_data(
                    request.get_json(force=force, silent=silent, cache=cache)
                )
                if g.request_data:  # request_data is "truthy" (non-empty)
                    logger.warn(
                        'Received request data: {0}'.format(g.request_data))

            except:
                raise errors.InvalidRequestData(
                    log_message='Error reading/normalizing JSON request data!')

        return g.request_data


def current_request_headers():
    try:
        return g.request_headers
    except AttributeError:
        g.request_headers = dict(request.headers)
        return g.request_headers

# def current_request_imei():
#     # return request.headers.get('Imei') or ''
#     return request.headers.get('Imei')

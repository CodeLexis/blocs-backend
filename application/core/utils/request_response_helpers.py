from flask import jsonify, make_response, request

from application.core.utils.contexts import (current_api_ref,
                                             current_request_data)
from application.core.utils.normalizers import normalize_json_data


SUCCESS_STATUS = 'SUCCESS'
FAILURE_STATUS = 'FAILURE'

SUCCESS_MESSAGE = 'Request completed successfully.'
FAILURE_MESSAGE = 'Unable to complete request.'


def get_request_headers():
    return request.headers


def get_request_ip():
    return (request.access_route[-1]
            or request.environ.get('HTTP_X_REAL_IP',
                                   request.remote_addr))


def get_request_pagination_params():
    return {
        'per_page': request.args.get('per_page'),
        'page': request.args.get('page')
    }

# def get_android_client_app_version():
#     return request.headers.get('Version')


# def get_request_imei():
#     # return request.headers.get('Imei') or ''
#     return request.headers.get('Imei')


def _make_api_response(status, response_data=None, message=None, code=200,
                       response_meta=None):
    """JSON-format the response for current request"""

    response_data = normalize_json_data(response_data)

    response_build = {
        'api_ref': current_api_ref(),
        'code': int(code),
        'message': message,
        'status': status,
        'your_request': current_request_data(),
        'your_response': response_data
    }

    try:
        response_build.update(response_meta)
    except TypeError:
        pass

    return make_response(jsonify(response_build), code)


def api_success_response(response_data, message=None, code=200,
                         response_meta=None):

    message = message or SUCCESS_MESSAGE

    return _make_api_response(status=SUCCESS_STATUS,
                              response_data=response_data,
                              message=message,
                              code=code,
                              response_meta=response_meta)


def api_failure_response(error_msg=None, code=200, response_meta=None):

    error_msg = error_msg or FAILURE_MESSAGE

    return _make_api_response(status=FAILURE_STATUS,
                              response_data=None,
                              message=error_msg,
                              code=code,
                              response_meta=response_meta)

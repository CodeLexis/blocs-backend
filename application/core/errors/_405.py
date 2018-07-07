from .base import APIError


_ERROR_CODE = 405  # HTTP method not allowed


class HTTPRequestMethodNotSupported(APIError):
    code = _ERROR_CODE
    message = 'You used an invalid HTTP method for this request.'

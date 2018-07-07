from .base import APIError


_ERROR_CODE = 408


class NetworkTimeout(APIError):
    code = _ERROR_CODE
    message = 'Request timed-out. Please try again.'

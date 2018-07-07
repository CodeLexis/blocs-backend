from .base import APIError


_ERROR_CODE = 498  # expired session token


class TokenExpired(APIError):
    code = _ERROR_CODE
    message = 'Your session is expired. Please re-authenticate.'

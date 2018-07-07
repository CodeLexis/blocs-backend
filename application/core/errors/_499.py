from .base import APIError


_ERROR_CODE = 417  # session token required


class TokenNotFound(APIError):
    code = _ERROR_CODE
    message = 'Token missing in request.'

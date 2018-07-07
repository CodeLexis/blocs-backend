from .base import APIError


_ERROR_CODE = 401  # unauthorized; disabled user


class UnauthorizedUser(APIError):
    code = _ERROR_CODE
    message = 'You are not authorized to carry out this operation.'


class UnsuccessfulAuthentication(UnauthorizedUser):
    message = 'Authentication was unsuccessful.'


class UserIPChanged(UnauthorizedUser):
    message = 'User IP has changed! Please re-authenticate.'


class InvalidToken(UnauthorizedUser):
    message = 'Invalid authentication token provided.'

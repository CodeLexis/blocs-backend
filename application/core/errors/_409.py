from .base import APIError


_ERROR_CODE = 409


class ResourceConflict(APIError):
    code = _ERROR_CODE
    message = 'Resource already exists'


class SavingsGoalExists(ResourceConflict):
    message = 'Account already has a Savings Goal.'


class ExistingTransaction(ResourceConflict):
    message = 'The transaction has already been sent.'

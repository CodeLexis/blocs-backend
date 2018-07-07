from .base import APIError


_ERROR_CODE = 403  # forbidden


class BudgetForAccountAlreadyExists(APIError):
    pass


class Forbidden(APIError):
    code = _ERROR_CODE
    message = 'Forbidden!'


# class PaymentOutOfRangeError(Forbidden):
#     message = ('Amount specified exceeds allowed amount for prepaid '
#                'vending.')


class SMSNotAllowed(Forbidden):
    message = 'SMS sending is not allowed.'


class InsufficientFunds(Forbidden):
    message = 'Account has insufficient funds for this transaction.'


class WithdrawalNotPermitted(Forbidden):
    message = 'Funds withdrawal is not permitted on this account.'

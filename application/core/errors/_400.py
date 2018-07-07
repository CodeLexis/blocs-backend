from .base import APIError


_ERROR_CODE = 400  # bad request


class BadRequest(APIError):
    code = _ERROR_CODE
    message = 'Request was not properly formatted.'


class InvalidRequestData(BadRequest):
    message = 'Invalid or incomplete request data.'


class InvalidAmountError(BadRequest):
    message = 'Invalid amount specified.'


class InvalidPhoneNumber(BadRequest):
    message = 'Invalid phone number provided.'


class InvalidPaymentChannel(BadRequest):
    message = 'Invalid payment channel value provided.'


class InvalidPaymentType(BadRequest):
    message = 'Invalid payment type value provided.'


# class InvalidPayRef(BadRequest):
#     message = ('Invalid `payRef` sent. Validate the customer, '
#                'then use the given `payRef` for payment.')


# class PasswordsDoNotMatch(BadRequest):
#     message = 'Password mismatch.'


# class InvalidUserCategory(BadRequest):
#     message = 'Could not find a User Category with the ID provided.'

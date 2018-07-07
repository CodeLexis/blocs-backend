from .base import APIError


_ERROR_CODE = 502  # bad gateway


class UpstreamServerError(APIError):
    code = _ERROR_CODE
    message = 'Bad Gateway!'


# class UpstreamPaymentError(UpstreamServerError):
#     message = ('UpstreamServerError, vending cannot be completed at '
#                'the moment, try later.')
#
#
# class UpstreamValidationError(UpstreamServerError):
#     message = ('UpstreamServerError, validation of customer cannot be '
#                'completed at the moment, try later.')
#
#
# class UpstreamRequeryError(UpstreamServerError):
#     message = ('UpstreamServerError, cannot confirm payment at '
#                'the moment, try later.')

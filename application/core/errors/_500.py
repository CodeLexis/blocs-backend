from .base import APIError, DEFAULT_ERROR_CODE, DEFAULT_ERROR_MESSAGE


_ERROR_CODE = DEFAULT_ERROR_CODE


class InternalServerError(APIError):
    code = _ERROR_CODE
    message = DEFAULT_ERROR_MESSAGE  # 'An internal server error occurred!'


class DBSaveError(InternalServerError):
    message = 'The provided data could not be persisted.'


class SMSSendingFailed(InternalServerError):
    message = 'Failed to send an SMS.'


# class FailedTransaction(InternalServerError):
#     message = 'Transaction failed, and was not saved.'

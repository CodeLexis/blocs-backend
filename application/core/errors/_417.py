from .base import APIError


_ERROR_CODE = 417


class ExpectationFailed(APIError):
    code = _ERROR_CODE
    message = "Could not satisfy client's 'Expect' request."

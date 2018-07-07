from .base import APIError


_ERROR_CODE = 204  # no content


# class NoPayRefGenerated(APIError):
#     code = _ERROR_CODE
#     message = (
#         'No payref was generated. Payment cannot be initiated '
#         'without payref.'
#     )

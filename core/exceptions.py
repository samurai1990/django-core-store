from django.utils.translation import gettext_lazy as _
from rest_framework.status import *
from rest_framework.exceptions import _get_codes, _get_error_details, _get_full_details
from .errors import *


class AnonymousUserAttempt(Exception):
    pass

class APIException(Exception):
    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')
    default_code = 'error'

    def __init__(self, detail=None, code=None):
        super().__init__()
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = _get_error_details(detail, code)

    def __str__(self):
        return str(self.detail)

    def get_codes(self):
        return _get_codes(self.detail)

    def get_full_details(self):
        return _get_full_details(self.detail)


class BaseApiExp(APIException):
    err_code = 0
    default_code = ''


class AuthenticationFailedExp(BaseApiExp):
    err_code = ERR_AUTHENTICATION_FAILED
    status_code = HTTP_401_UNAUTHORIZED


class MethodNotAllowedExp(BaseApiExp):
    err_code = ERR_METHOD_NOT_ALLOWED
    status_code = HTTP_405_METHOD_NOT_ALLOWED


class NotAcceptableExp(BaseApiExp):
    err_code = ERR_NOT_ACCEPTABLE
    status_code = HTTP_406_NOT_ACCEPTABLE


class NotFoundExp(BaseApiExp):
    err_code = ERR_DOT_NOT_EXIST
    status_code = HTTP_404_NOT_FOUND


class MethodNotAllowedExp(BaseApiExp):
    err_code = ERR_METHOD_NOT_ALLOWED
    status_code = HTTP_405_METHOD_NOT_ALLOWED


class PermissionDeniedExp(BaseApiExp):
    err_code = ERR_PERMISSION_DENIED
    status_code = HTTP_403_FORBIDDEN


class ReauthenticateExp(BaseApiExp):
    err_code = ERR_REAUTHENTICATE
    status_code = HTTP_403_FORBIDDEN


class ValidationErrorExp(BaseApiExp):
    err_code = ERR_INPUT_VALIDATION
    status_code = HTTP_400_BAD_REQUEST


class InternalError(BaseApiExp):
    err_code = ERR_INTERNAL
    status_code = HTTP_500_INTERNAL_SERVER_ERROR

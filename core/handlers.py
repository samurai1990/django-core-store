from traceback import format_exc
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import MethodNotAllowed, NotAcceptable
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import set_rollback
from . import exceptions  as apiexp
from . import errors


def exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = apiexp.NotFoundExp()
    elif isinstance(exc, PermissionDenied):
        exc = apiexp.PermissionDeniedExp()
    elif isinstance(exc, MethodNotAllowed):
        exc = apiexp.MethodNotAllowedExp(exc.default_detail)
    elif isinstance(exc, NotAcceptable):
        exc = apiexp.NotAcceptableExp(exc.default_detail)
    elif isinstance(exc, apiexp.BaseApiExp):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        data = {
            'err': True,
            'err_code': exc.err_code,
            'err_msg': exc.detail,
        }
        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

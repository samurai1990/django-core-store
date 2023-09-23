from uuid import UUID
from jwt import DecodeError, ExpiredSignatureError
from django.core.cache import caches
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from core.exceptions import (
    ReauthenticateExp,
    PermissionDeniedExp,
    NotFoundExp,
    AnonymousUserAttempt,
    )
from .models import User
from utils.jwt import JwtHelper
from django.core.exceptions import ValidationError


class Authentication(BaseAuthentication):
    def get_authorization_header(self, request):
        RAELM = 'token'
        auth_header = request.headers.get('Authorization', None)
        if auth_header is not None:
            raelm, token = auth_header.split(' ')
            if raelm == RAELM:
                return token
            else:
                raise PermissionDeniedExp(f'raelm {raelm} is not valid')
        else:
            raise AnonymousUserAttempt()

    def check_jwt_token(self, request):
        auth_header = self.get_authorization_header(request)
        jwt_token = self.get_decoded_jwt_token(auth_header)
        return self.get_user(user_id=jwt_token.get('user').get('user_id'))

    def get_decoded_jwt_token(self, token):
        is_valid_token = caches['token-cache'].get(token)
        if is_valid_token == 0:
            try:
                return JwtHelper.decode(token)
            except DecodeError as e:
                raise PermissionDeniedExp(f'malformed token')
            except ExpiredSignatureError as e:
                raise ReauthenticateExp(
                    f'token has expired. try to re-authenticate')
        else:
            raise ReauthenticateExp(
                f'not a valid token. try to re-authenticate')

    def check_api_token(self, request):
        try:
            api_token = request.headers.get('PRIVATE-API-KEY', None)
            if api_token is None:
                raise AnonymousUserAttempt()
            else:
                UUID(api_token)
                return self.get_user(api_token=api_token)
        except ValueError as e:
            raise ReauthenticateExp('malformed api token')

    def get_user(self, api_token=None, user_id=None):
        try:
            if user_id is not None:
                user = User.objects.get(id=user_id)
            elif api_token is not None:
                user = User.objects.get(profile__api_token=api_token)
            if user.is_active != True:
                raise PermissionDeniedExp(f'your account is not active')
            else:
                return user
        except ObjectDoesNotExist as e:
            raise NotFoundExp(f'User {user_id} not found')
        
    def get_user_with_api_key(self, api_key=None):
        try:
            if api_key is not None:
                user = User.objects.get(profile__api_token=api_key)
            if user.is_active != True:
                raise PermissionDeniedExp(f'your account is not active')
            else:
                return user
        except ValidationError as e:
            raise ReauthenticateExp(f'{api_key} not a valid api key.')
        except User.DoesNotExist :
            raise ReauthenticateExp(f'{api_key} not a valid api key.')
        
    def get_api_key_header(self, request):
        auth_header = request.headers.get('Api-Key', None)
        if auth_header is not None:
                return auth_header
        else:
            raise AnonymousUserAttempt()
        
    def check_api_key(self, request):
        return self.get_user_with_api_key(request.headers.get('API-KEY', None))
                                    
    def authenticate(self, request):
        try:
            if 'Authorization' in request.headers.keys():
                user=self.check_jwt_token(request)
            elif 'Api-Key' in request.headers.keys() :
                user=self.check_api_key(request)
            else:
                user=self.check_api_token(request)
            return (user,None)
        except AnonymousUserAttempt as e:
            return (AnonymousUser(), None)

from uuid import uuid4
from core.base_viewset import BaseViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from core.decorators import serializer_validation
from core.mixins import IdempotentUpdateMixin
from rest_framework.permissions import AllowAny
from .permissions import IsAdmin, IsAuthenticatedAndOwner
from .filters import (
    ActiveUserFilterBackend,
    DeletedUserFilterBackend,
    SuperUserFilterBackend)
from .models import User
from .signals import user_logged_out, regenerate_token
from .serializers import (
    UserSignUpRequest,
    UserSignUpResponse,
    UserSignInRequest,
    UserListResponse,
    UserRetrieveResponse,
    UserChangePasswordRequest,
    UserProfileResponse,
    UserUpdateRequest,
    UserUpdateResponse,
    UserPartialUpdateRequest,
    UserPartialUpdateResponse,
    UserSignInResponse)


class UserViewSet(IdempotentUpdateMixin, BaseViewSet):
    queryset = User.objects.all()
    serializer_action_classes = {
        'create': {
            'req': UserSignUpRequest,
            'res': UserSignUpResponse,
        },
        'signin': {
            'req': UserSignInRequest,
            'res': UserSignInResponse,
        },
        'list': {
            'res': UserListResponse,
        },
        'change_password': {
            'req': UserChangePasswordRequest,
        },
        'retrieve': {
            'res': UserRetrieveResponse,
        },
        'profile': {
            'res': UserProfileResponse,
        },
        'update': {
            'req': UserUpdateRequest,
            'res': UserUpdateResponse,
        },
        'partial_update': {
            'req': UserPartialUpdateRequest,
            'res': UserPartialUpdateResponse,
        },
    }
    permission_action_classes = {
        'create': [AllowAny, ],
        'signin': [AllowAny, ],
        'signout': [AllowAny, ],
        'list': [IsAdmin, ],
        'retrieve': [IsAdmin, ],
        'change_password': [IsAuthenticatedAndOwner, ],
        'profile': [IsAuthenticatedAndOwner, ],
        'update': [IsAuthenticatedAndOwner, ],
        'partial_update': [IsAdmin, ],
        'destroy': [IsAuthenticatedAndOwner | IsAdmin, ],
        'regen_token': [IsAuthenticatedAndOwner, ],
    }
    filter_backends = [
        ActiveUserFilterBackend,
        DeletedUserFilterBackend,
        SuperUserFilterBackend,
     ]

    def get_queryset(self):
        if self.action == 'list' or self.action == 'partial_update':
            qs = User.allobjects.all()
            return qs
        else:
            return super().get_queryset()

    @action(detail=False, methods=['POST'],
            url_name='signin', url_path='signin')
    @serializer_validation
    def signin(self, request, *args, **kwargs):
        reqser = self.get_serializer(data=request.data)
        reqser.is_valid(raise_exception=True)
        user = reqser.login(self.queryset)
        resser = self.get_serializer_response()(user)
        return Response(data={user.__class__.__name__.lower(): resser.data})

    @action(detail=False, methods=['GET'],
            url_name='signout', url_path='signout')
    def signout(self, request, *args, **kwargs):
        user_logged_out.send(sender=User, request=request)
        return Response(data={})

    @action(detail=False, methods=['POST'],
            url_name='change-password', url_path='change-password')
    @serializer_validation
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.change_password(self.queryset, request, id=request.user.id)
        return Response(data={})

    @action(detail=False, methods=['GET'],
            url_name='profile', url_path='profile')
    def profile(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer_response()(instance)
        return Response(
            data={instance.__class__.__name__.lower(): serializer.data})

    @action(detail=False, methods=['GET'],
            url_name='regenerate-token', url_path='regenerate-token')
    def regen_token(self, request, *args, **kwargs):
        regenerate_token.send(sender=User, user=request.user)
        return Response(data={})

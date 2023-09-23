from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from core.exceptions import NotFoundExp, ValidationErrorExp, AuthenticationFailedExp
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import User, UserProfile
from .signals import user_logged_in, user_login_failed, user_logged_out


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['api_token']


class UserSignUpRequest(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
            instance.access_token = user_logged_in.send(
                sender=User, user=instance)[0][1]
            return instance
        except IntegrityError as e:
            raise ValidationErrorExp(f'User is already exists')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserSignUpResponse(WritableNestedModelSerializer):
    profile = UserProfileSerializer()
    access_token = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'is_active', 'is_superuser', 'profile', 'access_token']


class UserSignInRequest(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def login(self, queryset):
        username = self.validated_data.get('username')
        password = self.validated_data.get('password')
        try:
            user = queryset.get(username=username)
            if user.check_password(password):
                if user.is_active == False and user.failed_login_tries >= 3:
                    elapsed_time = timezone.now()-user.banned_at
                    if elapsed_time >= timedelta(hours=2):
                        user.activate()
                    else:
                        raise AuthenticationFailedExp(
                            f'Your account has been inactive for 2 hours. If you have an emergency contact administrator')
                user.access_token = user_logged_in.send(
                    sender=User, user=user)[0][1]
                return user
            else:
                user_login_failed.send(sender=User, user=user)
                raise AuthenticationFailedExp(f'Invalid Credentials')
        except ObjectDoesNotExist as e:
            raise NotFoundExp(f'User not found')


class UserSignInResponse(UserSignUpResponse):
    class Meta(UserSignUpResponse.Meta):
        pass


class UserListResponse(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'is_active',
            'is_superuser',
            'last_login',
            'is_deleted',
            'created']


class UserChangePasswordRequest(serializers.ModelSerializer):
    old_password = serializers.CharField(
        write_only=True,
        required=True,
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
    )

    def change_password(self, queryset, request, id):
        old_password = self.validated_data.get('old_password')
        new_password = self.validated_data.get('new_password')
        try:
            user = queryset.get(id=id)
            if user.check_password(old_password):
                user.set_password(new_password)
                user_logged_out.send(sender=User, request=request)
                return True
            else:
                raise ValidationErrorExp(f'old password does not matched')
        except ObjectDoesNotExist as e:
            raise NotFoundExp(f'Invalid user')

    class Meta:
        model = User
        fields = ['new_password', 'old_password']


class UserRetrieveResponse(UserSignUpResponse):
    class Meta(UserSignUpResponse.Meta):
        pass


class UserProfileResponse(WritableNestedModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'is_superuser']


class UserUpdateRequest(WritableNestedModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']


class UserUpdateResponse(WritableNestedModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']


class UserPartialUpdateRequest(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'is_active',
            'is_superuser',
            'is_deleted',
            'failed_login_tries']


class UserPartialUpdateResponse(UserPartialUpdateRequest):
    class Meta(UserPartialUpdateRequest.Meta):
        pass

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from core.base_model import BaseModel
from .managers import UserManager, SuperUserManager


class AbstractUser(AbstractBaseUser, BaseModel):
    username_validator = UnicodeUsernameValidator()
    last_login = models.DateTimeField(null=True)
    failed_login_tries = models.PositiveSmallIntegerField(default=0)
    banned_at = models.DateTimeField(null=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        verbose_name='Email Address', max_length=254, unique=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)

    USERNAME_FIELD = 'username'
    # email and password are required by default
    REQUIRED_FIELDS = ['email']

    objects = UserManager()
    allobjects = SuperUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = True

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class User(AbstractUser):
    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.failed_login_tries = 0
        self.save()

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-last_login', '-created']
        indexes = [
            models.Index(fields=['is_deleted'])
        ]


class UserProfile(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile')
    api_token = models.UUIDField(null=True, blank=True)

    class Meta:
        db_table = 'profiles'
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

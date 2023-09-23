from uuid import uuid4
from django.core.cache import caches
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from utils.jwt import JwtHelper
from ..models import User, UserProfile
from .signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
    regenerate_token,
    )


@receiver(post_save, sender=User)
def create_profile(sender, instance: User, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance,api_token=str(uuid4()))


@receiver(regenerate_token, sender=User)
def generate_api_token(sender, user: User, **kwargs):
    user.profile.api_token = str(uuid4())
    user.profile.save()


@receiver(user_logged_in, sender=User)
def set_auth_token(sender, user: User, **kwargs):
    user_fields = {
                'user_id': str(user.id)
    }
    token = JwtHelper.encode({'user': user_fields})
    caches['token-cache'].set(token, 0)
    return token


@receiver(user_logged_in, sender=User)
def update_user_last_login(sender, user: User, **kwargs):
    user.last_login = timezone.now()
    user.save()


@receiver(user_logged_out, sender=User)
def delete_auth_token(sender, request, **kwrargs):
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        caches['token-cache'].delete(token)
    except (AttributeError, IndexError) as e:
        pass


@receiver(user_login_failed, sender=User)
def count_failed_login_tries(sender, user: User, **kwargs):
    user.failed_login_tries += 1
    if user.failed_login_tries == 3:
        user.is_active = False
        user.banned_at = timezone.now()
    user.save()

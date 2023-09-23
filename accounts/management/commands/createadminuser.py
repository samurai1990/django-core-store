from django.core.management.base import BaseCommand
from logging import getLogger
from accounts.models import User
from os import getenv
logger = getLogger('django')


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = getenv('SUPER_USERNAME')
        password = getenv('SUPER_PASSWORD')
        try:
            user = User.allobjects.get(username=username)
            if user is not None:
                logger.info(f'user "{username}" is exist')
        except Exception:
            logger.info(f'##### user: "{username}" created. #####')
            User.objects.create_superuser(
                username=username,
                password=password,
                email=f"{username}@co.com")
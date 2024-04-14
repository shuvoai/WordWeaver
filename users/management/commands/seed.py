from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
User = get_user_model()


class Command(BaseCommand):
    help = 'Created a Super User.'

    def handle(self, *args, **kwargs):
        username = 'superadmin'
        password = "superadmin@word_weaver"
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            User.objects.create_superuser(
                username=username,
                password=password
            )

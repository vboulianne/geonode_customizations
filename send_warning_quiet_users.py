from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Send users a reminded to log once in a while'

    def handle(self, *args, **options):

        all_users = User.objects.filter()
        for user in all_users:
            formatted_time = user.last_login.astimezone().strftime("%d.%m.%Y %H:%M:%S")


            self.stdout.write(f"{user.username} | E-mail {user.email} | Last Login: {formatted_time}")


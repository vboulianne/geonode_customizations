from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'List all currently logged in users'

    def handle(self, *args, **options):
        sessions = Session.objects.filter(expire_date__gte=timezone.now())

        uid_list = []
        for session in sessions:
            data = session.get_decoded()
            uid = data.get('_auth_user_id', None)
            if uid:
                uid_list.append(uid)

        logged_in_users = User.objects.filter(id__in=uid_list)
        for user in logged_in_users:
            formatted_time = user.last_login.astimezone().strftime("%d.%m.%Y %H:%M:%S")
            self.stdout.write(f"{user.username} | E-mail {user.email} | Last Login: {formatted_time}")


from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user_profile.models import Profile

class Command(BaseCommand):
    help = 'Creates user profiles for users that don\'t have one'

    def handle(self, *args, **kwargs):
        users = User.objects.filter(profile__isnull=True)
        for user in users:
            Profile.objects.create(user=user)
            self.stdout.write(f'Created profile for user: {user.username}')

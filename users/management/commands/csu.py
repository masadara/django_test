
from django.core.management import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        email = 'adminn@gmail.com'
        password = 'qq1234'
        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Пользователь с email {email} уже существует.'))
            return
        user = CustomUser(
            email=email,
            username=email.split('@')[0]
        )
        user.set_password('qq1234')
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
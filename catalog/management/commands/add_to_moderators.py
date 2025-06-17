from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Добавляет пользователя в группу "Модератор продуктов"'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Имя пользователя')

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
            group, created = Group.objects.get_or_create(name='Модератор продуктов')
            user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f'Пользователь {username} добавлен в группу модераторов.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Пользователь не найден.'))

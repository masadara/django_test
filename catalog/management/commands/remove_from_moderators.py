from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Удаляет пользователя из группы "Модератор продуктов"'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Имя пользователя')

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
            group = Group.objects.get(name='Модератор продуктов')
            user.groups.remove(group)
            self.stdout.write(self.style.SUCCESS(f'Пользователь {username} удалён из группы модераторов.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Пользователь не найден.'))
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR('Группа не найдена.'))

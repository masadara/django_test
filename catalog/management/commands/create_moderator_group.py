from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from catalog.models import Product

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        can_unpublish_product = Permission.objects.get(codename='can_unpublish_product')
        delete_product_permission = Permission.objects.get(codename='delete_product')

        group.permissions.add(can_unpublish_product, delete_product_permission)

        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана и права назначены.'))
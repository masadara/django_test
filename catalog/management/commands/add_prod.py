from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Add test to the database'

    def handle(self, *args, **kwargs):
        cat, _ = Category.objects.get_or_create(name='Диваны')
        Product.objects.all().delete()
        prods = [
            {'name': 'Диван2', 'created_at': '1904-01-01 05:05:05', 'sell_price': 100, 'category': cat},
            {'name': 'Диван1', 'created_at': '1901-01-01 05:05:05', 'sell_price': 100, 'category': cat},
        ]

        for prod_data in prods:
            prod, created = Product.objects.get_or_create(**prod_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added book: {prod.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Book already exists: {prod.name}'))
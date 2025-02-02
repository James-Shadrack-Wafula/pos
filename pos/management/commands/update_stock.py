import random
from django.core.management.base import BaseCommand
from pos.models import Item

class Command(BaseCommand):
    help = 'Update stock quantity for items with missing or zero stock'

    def handle(self, *args, **kwargs):
        items = Item.objects.all()
        updated_count = 0

        for item in items:
            if item.stock_quantity is None or item.stock_quantity == 0:
                item.stock_quantity = random.randint(1, 100)  # Assign a random value
                item.save()
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} items with new stock quantities'))

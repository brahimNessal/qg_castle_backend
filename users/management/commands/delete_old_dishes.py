from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import Dish
from datetime import timedelta

class Command(BaseCommand):
    help = 'Delete dishes from yesterday'

    def handle(self, *args, **kwargs):
        yesterday = timezone.now().date() - timedelta(days=1)
        deleted_count, _ = Dish.objects.filter(created_at__date=yesterday).delete()
        self.stdout.write(f'Deleted {deleted_count} dishes from {yesterday}')

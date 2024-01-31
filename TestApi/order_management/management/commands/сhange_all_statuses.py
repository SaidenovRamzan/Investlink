from django.core.management.base import BaseCommand
from order_management.models import Order


class Command(BaseCommand):
    help = 'Changing status on "new"'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Change all status in Postgres on "new"...'))
        for order in Order.objects.all():
            order.status = 'new'
            order.save()

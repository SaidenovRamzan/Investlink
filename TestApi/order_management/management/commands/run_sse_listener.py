from django.core.management.base import BaseCommand
from order_management.tasks import listen_sse_events
import time


class Command(BaseCommand):
    help = 'Runs the SSE listener task'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting the SSE listener task...'))
        time.sleep(50)
        listen_sse_events.delay()

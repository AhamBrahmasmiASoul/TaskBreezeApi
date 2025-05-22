from django.core.management.base import BaseCommand
from jobscheduler.scheduler import start

class Command(BaseCommand):
    help = "Starts the APScheduler background scheduler."

    def handle(self, *args, **options):
        self.stdout.write("🔄 Starting scheduler from management command...")
        start()

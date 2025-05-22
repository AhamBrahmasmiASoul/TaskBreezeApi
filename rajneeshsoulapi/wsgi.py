"""
WSGI config for rajneeshsoulapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from jobscheduler.scheduler import scheduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rajneeshsoulapi.settings')

application = get_wsgi_application()

# Add this to gracefully stop the scheduler when shutting down the server
def shutdown_scheduler(signal, frame):
    scheduler.shutdown()
    print("Scheduler shutdown gracefully")
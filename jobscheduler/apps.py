import os

from django.apps import AppConfig
import threading

class JobschedulerConfig(AppConfig):
    name = 'jobscheduler'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true' and threading.current_thread().name == "MainThread":
            from .scheduler import start
            start()
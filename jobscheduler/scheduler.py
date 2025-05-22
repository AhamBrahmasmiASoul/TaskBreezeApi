import threading
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import atexit

scheduler = BackgroundScheduler()

def my_scheduled_task():
    from rajneehsoulapiapp.core.perform import trigger_task
    print(f"🔁 Running scheduled task at {datetime.now()}")
    trigger_task()


def start():
    if not scheduler.running:
        print("🟢 Starting APScheduler...")

        scheduler.add_job(
            my_scheduled_task,
            trigger=IntervalTrigger(minutes=1),
            id="trigger_task_job",
            replace_existing=True,
        )

        # Delay first call by 5 seconds
        threading.Thread(target=lambda: (time.sleep(5), my_scheduled_task())).start()

        scheduler.start()
        atexit.register(lambda: scheduler.shutdown(wait=False))
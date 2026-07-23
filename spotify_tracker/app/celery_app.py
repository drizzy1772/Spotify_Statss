


from celery import Celery
from celery.schedules import crontab
import os


redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery(
    "analytics_worker",
    broker=redis_url,
    backend=redis_url,
    include=["app.tasks.pipeline"])

celery_app.conf.beat_schedule = {
    "task": 'proj.tasks.send_report',
    'schedule': crontab(hour=0, minute=0)
}

celery_app.conf.timezone = "Europe/Kyiv"

celery_app.conf.beat_schedule = {
    'sync-stats-every-midnight': {
        'task': 'app.tasks.pipeline.sync_daily_spotify_stats',
        'schedule': crontab(minute=0, hour=0)
    }
}
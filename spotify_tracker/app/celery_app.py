


from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "spotify_stats",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.tasks"])


celery_app.conf.timezone = "Europe/Kyiv"

celery_app.conf.beat_schedule = {
    'sync-stats-every-midnight': {
        'task': 'app.tasks.run_sync_daily_stats_task',
        'schedule': crontab(minute=0, hour=0)
    }
}
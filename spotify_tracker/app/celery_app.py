


from celery import Celery

celery_app = Celery("spotify_stats", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

celery_app.conf.beat_schedule = {
    
}
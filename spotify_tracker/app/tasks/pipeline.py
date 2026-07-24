






from app.celery_app import celery_app
from app.database import SessionLocal
from app.crud import batch_upsert_track_stats
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="sync_daily_spotify_stats")
def sync_daily_spotify_starts():
    logger.info("Starting a synchronization stat from Spotify")
    
    db = SessionLocal()
    
    try:
        raw_data = get_spotify_stats()
        
        
        
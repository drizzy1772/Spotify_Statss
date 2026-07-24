







import logging
import asyncio

from app.celery_app import celery_app
from app.services.spotify import get_tracks_batch_stats
from app.database import SessionLocal
from app.crud import batch_upsert_track_stats

logger = logging.getLogger(__name__)

def get_all_tracked_ids(db) -> list[str]:
    return ["1xK1Gg9SxG8s2cg46sEAIG", "7ouMYZxgJACzhB5Z8Z2B7p"]


@celery_app.task(name="sync_daily_spotify_stats")
def sync_daily_spotify_stats():
    logger.info("Starting synchronization stats from Spotify")
    
    db = SessionLocal()
    
    try:
        track_ids = get_all_tracked_ids(db)
        
        if not track_ids:
            logger.info("There is no tracks")
            return
    
        logger.info(f"Collecting stats for {len(track_ids)} tracks...")
    
        formatted_data = asyncio.run(get_tracks_batch_stats(track_ids))    
        
        logger.info(f"Successfully saved stats for {len(formatted_data)} tracks")
        
    except Exception as e:
        logger.error(f"Mistake when pipeline started: {e}")
    
    finally:
        db.close()
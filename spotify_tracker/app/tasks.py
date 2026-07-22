






import asyncio
from app.celery_app import celery_app
from app.sync import sync_daily_stats
from app.database import async_session
import redis
from datetime import date
from app.celery_app import celery_app
from app.database import SessionLocal
from app.models import TrackDailyStats
from sqlalchemy.dialects.postgresql import insert

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


@celery_app.task(name="app.tasks.run_sync_daily_stats_task")
def run_sync_daily_stats_task():
    
    data = r.hgetall("redis_key_name")
    
    if not data:
        return "No data to sync in Redis."
    
    today = date.today()
    db = SessionLocal()
    
    
    try:
        for track_id_str, count_str in data.items():
            track_id = int(track_id_str)
            play_count = int(count_str)
            stmt = insert(TrackDailyStats).values(track_id=track_id, date=today, play_count=play_count)
            upper_stmt = stmt.on_conflict_do_update(
                index_elements=["track_id", "date"],
                set_=dict(play_count=TrackDailyStats.play_count + stmt.excluded.play_count)
                
            )
            db.execute(upper_stmt)
            
        db.commit()
        
        
        r.delete("redis_key_name")
    
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

    return f"Successfully synced tracks to PostgreSql"

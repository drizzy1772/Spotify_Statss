






import datetime
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from app.db_models import TrackDailyStats

def batch_upsert_track_stats(db: Session, stats_data: list[dict]):
    if not stats_data:
        return
    
    
    stmt = insert(TrackDailyStats).values(stats_data)
    
    upsert_stmt = stmt.on_conflict_do_update(
        index_elements=["track_id", "date"],
        set_={
            "play_count": stmt.excluded.play_count
        }
    )

    db.execute(upsert_stmt)
    db.commit()
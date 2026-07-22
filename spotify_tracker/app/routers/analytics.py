






from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TrackDailyStats


router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/tracks/{track_id}/stats")
def get_track_analytics(track_id: int, db: Session = Depends(get_db)):
    track_stats = db.query(TrackDailyStats).filter(TrackDailyStats.track_id == track_id).all()
    
    if not track_stats:
        raise HTTPException(status_code=404, detail="Stats not found for this track")
    
    return {
        "track_id": track_id,
        "daily_stats": track_stats
    }
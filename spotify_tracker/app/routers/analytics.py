






from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TrackDailyStats
from app.services.spotify import get_track_metadata
from app.api.dependencies import check_rate_limit

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/tracks/{track_id}/stats", dependencies=[Depends(check_rate_limit)])
async def get_track_analytics(track_id: str, db: Session = Depends(get_db)):
    track_stats = db.query(TrackDailyStats).filter(TrackDailyStats.track_id == track_id).all()
    
    if not track_stats:
        raise HTTPException(status_code=404, detail="Stats not found for this track")
    
    track_info = await get_track_metadata(str(track_id))
    
    return {
        "track_id": track_id,
        "info": track_info,
        "daily_stats": track_stats
    }
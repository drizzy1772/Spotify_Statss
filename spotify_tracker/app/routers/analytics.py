






from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import TrackDailyStats
from app.services.spotify import get_cached_spotify_track
from app.routers.dependencies import check_rate_limit
from app.routers.dependencies import get_redis

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/tracks/{track_id}/stats", dependencies=[Depends(check_rate_limit)])
async def get_track_analytics(
    track_id: str, 
    db: Session = Depends(get_db),
    redis_client = Depends(get_redis)):
    
    track_stats = db.query(TrackDailyStats).filter(TrackDailyStats.track_id == track_id).all()
    
    if not track_stats:
        raise HTTPException(status_code=404, detail="Stats not found for this track")
    
    track_info = await get_cached_spotify_track(track_id, redis_client)
    
    if not track_info:
        raise HTTPException(status_code=404, detail="Track info was not found in Spotify")
    
    return {
        "track_id": track_id,
        "info": track_info,
        "daily_stats": track_stats
    }
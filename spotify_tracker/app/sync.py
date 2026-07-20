


from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import redis.asyncio as redis
from app.redis_client import redis_client
import requests
from app.redis_client import saving_token
import os
import db
import httpx
from app.models import SpotifyToken
from app.redis_client import redis_client
from app.models import TrackDailyStats
from sqlalchemy.dialects.postgresql import insert


async def sync_daily_stats(db: AsyncSession):
    t = date.today().isoformat()
    redis_key_name = f"listens:{t}"
    redis_data = await redis_client.hgetall(redis_key_name)
    if not redis_data:
        return
    
    db_data_list = []

    for track_id, listen_count in redis_data.items():
        slovarik = {
        "track_id": int(track_id),
        "event_date": t,
        "listen_count": int(listen_count)
    }    
        db_data_list.append(slovarik)
    
    stmt = insert(TrackDailyStats).values(db_data_list)
    
    upsert_stmt = stmt.on_conflict_do_update(
        index_elements=['track_id', 'event_date'],
        set_ = {
            'listen_count':TrackDailyStats.listen_count + stmt.excluded.listen_count
    }
)
    
    
    await db.execute(upsert_stmt)
    await db.commit()
    await redis_client.delete(redis_key_name)
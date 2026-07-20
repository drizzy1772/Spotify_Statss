





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

from fastapi import HTTPException, status

async def get_valid_access_token(
    db: AsyncSession
):
    token = await redis_client.get("spotify_access_token")
    
    if token is not None:
        return token
    
    elif token is None:
        statement = select(SpotifyToken).order_by(SpotifyToken.created_at.desc()).limit(1)
        
        result = await db.execute(statement)
        
        token_record = result.scalars().first()
        
        
    if token_record is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token was not recorded"
        )

    async with httpx.AsyncClient() as client:
        r = await client.post("https://accounts.spotify.com/api/token", data = {
        "grant_type": "refresh_token",
        "refresh_token": token_record.refresh_token,
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET")
    })
    
    
    data = r.json()
    new_access_token = data.get("access_token")
    new_expires_in = data.get("expires_in")
    new_refresh_token = data.get("refresh_token")
    
    if new_refresh_token:
        token_record.refresh_token = new_refresh_token
    

    await db.commit()
    await saving_token(new_access_token, new_expires_in)
    return new_access_token






import httpx
import base64
import os
from fastapi import HTTPException, status
import json

CACHE_TTL = 3600

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

async def get_spotify_token() -> str:
    
    url = "https://accounts.spotify.com/api/token"
    
    credentials = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
        "utf-8"
    )
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    data = {
        "grant_type": "client_credentials"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="status_code != 200")
        else:
            data = response.json()
            token = data["access_token"]
            return token

async def get_track_metadata(track_id: str) -> dict:
    token = await get_spotify_token()
    
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    
    headers = {
        "Authorization": f'Bearer {token}'
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            data = response.json()
    
    return {
        "name": data.get("name"),
        "artist": data["artists"][0]["name"] if data.get("artists") else "Unknown",
        "album_cover": data["album"]["images"][0]["url"] if data.get("album") and data["album"]["images"] else None,
    }
    
async def get_cached_spotify_track(track_id: str, redis_client):
    cache_key = f"spotify:track:{track_id}"

    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    track_data = await get_track_metadata(track_id)
    
    if not track_data:
            return None
        
    await redis_client.set(cache_key, json.dumps(track_data), ex=CACHE_TTL)

    return track_data
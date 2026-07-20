

import urllib.parse
import secrets
from fastapi import FastAPI, Response,  Cookie, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx
from app.database import get_db
from app.models import SpotifyToken
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta, date
from app.redis_client import saving_token, redis_client

load_dotenv()
app = FastAPI()



@app.get("/login")
async def login():
    user_state = secrets.token_urlsafe(16)

    print("CLIENT_ID", os.getenv("SPOTIFY_CLIENT_ID"))
    print("REDIRECT_URI", os.getenv("SPOTIFY_REDIRECT_URI"))
    
    params = {
        "response_type": "code",
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "scope": "user-read-currently-playing user-read-playback-state",
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
        "state": user_state
    }
    
    query_string = urllib.parse.urlencode(params)
    print(query_string)
    
    base_url = "https://accounts.spotify.com/authorize?"
    full_url = base_url + query_string
    print(full_url)   

    response = RedirectResponse(url=full_url, status_code=301)
    response.set_cookie(
        key="state",
        value=user_state,
    )
    return response

@app.get("/callback")
async def search_items(
    code: str,
    state: str,
    state_cookie: str | None = Cookie(alias="state"),
    db: AsyncSession = Depends(get_db)
):
    if not state_cookie:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cookie with state is empty bruh"
        )
    
    if not secrets.compare_digest(state, state_cookie):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Mistake of security state is not compare"
        )

    async with httpx.AsyncClient() as client:
        r = await client.post(url="https://accounts.spotify.com/api/token", data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET")
    })
        
        data = r.json()
        refresh_token = data.get("refresh_token")
        access_token = data.get("access_token")
        expires_in = data.get("expires_in")
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)    
        spotify_token = SpotifyToken(refresh_token=refresh_token, access_token=access_token, expires_at=expires_at)
        db.add(spotify_token)
        await db.commit()
        await saving_token(access_token, expires_in)
        print(refresh_token)
        print(access_token)
        print(expires_in)
        print(expires_at)
    return {"code": code, "state": state, "status": "verified"}
 
@app.post("/listen/{track_id}")
async def listening_tracker(track_id: int):
    t = date.today().isoformat()
    redis_key_name = f"listens:{t}"
    await redis_client.hincrby(
        name=redis_key_name,
        key=track_id,
        amount=1,
    )
    
    return {"status": "ok", "track_id": track_id}

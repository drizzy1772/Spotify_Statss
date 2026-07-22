





import httpx
import base64
import os
from fastapi import HTTPexception

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "0065574e049146cfa120c8a8c027861f")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "da44283c1de54e12b5fd7c5b65d293f9")

async def get_spotify_token() -> str:
    
    url = "https://accounts.spotify.com/api/token"
    
    text = "client_id:client_secret"
    b64 = base64.b64encde(text.encode()).decode()

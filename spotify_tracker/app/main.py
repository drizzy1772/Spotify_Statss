

import urllib.parse
import secrets
from fastapi import FastAPI, Response,  Cookie, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()

@app.get("/login")
async def login():
    user_state = secrets.token_urlsafe(16)

    params = {
        "response_type": "code",
        "client_id": "1",
        "scope": "user-read-currently-playing user-read-playback-state",
        "redirect_uri": "http://127.0.0.1:8000/callback",
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
    state_cookie: str | None = Cookie(alias="state") 
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
        
    return {"code": code, "state": state, "status": "verified"}
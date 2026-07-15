


import urllib.parse
import secrets
from fastapi import FastAPI, Response,  Cookie, HTTPException, status
from fastapi.responses import RedirectResponse

app = FastAPI()

user_state = secrets.token_urlsafe(16)


params = {
    "response_type": "code",
    "client_id": "123",
    "scope": "read",
    "redirect_uri": "http://127.0.0.1:8000/callback",
}

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
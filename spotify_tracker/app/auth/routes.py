


import urllib.parse
import secrets
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

user_state = secrets.token_urlsafe(16)


params = {
    "response_type": "json",
    "client_id": "123",
    "scope": "read",
    "redirect_uri": "http://127.0.0.1:8000/callback",
    "state": user_state
}

@app.get("/redirect")
async def redirecting_to_new():
    return RedirectResponse(url="/new-route")
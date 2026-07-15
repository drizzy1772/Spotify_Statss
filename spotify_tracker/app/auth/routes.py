


import urllib.parse
import secrets

user_state = secrets.token_urlsafe(16)


params = {
    "response_type": "json",
    "client_id": "123",
    "scope": "read",
    "redirect_uri": "http://127.0.0.1:8000/callback",
    "state": user_state
}
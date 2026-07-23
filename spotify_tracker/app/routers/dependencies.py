







from fastapi import Request, HTTPException
from app.db import redis_client
import redis
from fastapi import status

RATE_LIMIT = 30
RATE_LIMIT_WINDOW = 60

async def check_rate_limit(request: Request):
    client_ip = request.client.host
    redis_key = f"rate_limit:{client_ip}"

    current_count = int(redis_client.get(redis_key) or 0)
    
    if current_count >= RATE_LIMIT:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)
    
    new_val = redis_client.incr(redis_key)
    print(new_val)
    
    
    if current_count == 0:
        redis_client.expire(redis_key, RATE_LIMIT_WINDOW)
    
    return True
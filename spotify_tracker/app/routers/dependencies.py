







from fastapi import Request, HTTPException, Depends
from app.redis_client import redis_client
import redis
from fastapi import status
import json
from redis.asyncio import Redis
import httpx
from typing import AsyncGenerator

RATE_LIMIT = 30
RATE_LIMIT_WINDOW = 60

async def get_redis():
    yield redis_client

async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    client = httpx.Client(timeout=30.0)
    try:
        yield client
    finally:
        client.close()

async def check_rate_limit(user_id: str, redis: Redis = Depends(get_redis)):
    await redis.get(user_id)

    raw_value = await redis_client.get(redis_key)
    current_count = int(raw_value or 0)
    
    if current_count >= RATE_LIMIT:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)
    
    new_val = await redis_client.incr(redis_key)
    print(new_val)
    
    
    if current_count == 0:
        await redis_client.expire(redis_key, RATE_LIMIT_WINDOW)
    
    return True
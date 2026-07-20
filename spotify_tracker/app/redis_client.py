




import redis.asyncio as redis
import os

host = os.environ.get("REDIS_HOST", "localhost")
port = os.environ.get("REDIS_PORT", "6379")

redis_client = redis.Redis(host=host, port=int(port), decode_responses=True)

async def saving_token(
    token: str,
    expires_in: int,
) -> None:
    await redis_client.set("spotify_access_token", token, ex=expires_in)


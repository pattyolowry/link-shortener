import redis.asyncio as redis
import os

redis_client = redis.from_url(
    os.getenv("REDIS_URL", None),
    decode_responses=True,
)
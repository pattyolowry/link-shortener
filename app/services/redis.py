from redis import Redis
import os

redis_client = Redis.from_url(
    os.getenv("REDIS_URL", None),
    decode_responses=True,
    max_connections=100,
)
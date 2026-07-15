from typing import Optional, Callable
from sqlalchemy import text
from sqlmodel import Session
from .redis import redis_client

CACHE_TTL_SECONDS = 172800

def get_full_url(short_id: str, session_factory: Callable[[], Session]) -> Optional[str]:

    cache_key = f"link:{short_id}"
    cached_url = redis_client.get(cache_key)

    if cached_url is not None:
        return cached_url

    with session_factory() as session:
        full_url = get_url_from_postgres(short_id, session)

    if full_url is not None:
        redis_client.set(cache_key, full_url, ex=CACHE_TTL_SECONDS)

    return full_url


def get_url_from_postgres(short_id: str, session: Session) -> Optional[str]:
    result = session.exec(
        text("SELECT full_url FROM links WHERE short_id = :short_id"),
        params={"short_id": short_id},
    ).first()

    if result is None:
        return None
    
    return result[0]
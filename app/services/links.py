from typing import Optional, Callable
from sqlalchemy import text
from sqlmodel import Session

def get_full_url(short_id: str, session_factory: Callable[[], Session]) -> Optional[str]:

    # TODO: first check redis cache for url

    with session_factory() as session:
        full_url = get_url_from_postgres(short_id, session)
    return full_url


def get_url_from_postgres(short_id: str, session: Session) -> Optional[str]:
    result = session.exec(
        text("SELECT full_url FROM links WHERE short_id = :short_id"),
        params={"short_id": short_id},
    ).first()

    if result is None:
        return None
    
    return result[0]
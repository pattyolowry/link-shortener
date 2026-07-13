import os
from sqlmodel import Session, create_engine
from typing import Callable

DATABASE_URL = os.getenv(
    "DATABASE_URL", None
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=5,
    pool_timeout=3,
)

def get_session():
    with Session(engine) as session:
        yield session

def get_session_factory() -> Callable[[], Session]:
    return lambda: Session(engine)
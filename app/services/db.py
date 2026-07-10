import os
from sqlmodel import Session, create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL", None
)

engine = create_engine(DATABASE_URL, echo=False, pool_size=4, max_overflow=4, pool_timeout=3)

def get_session():
    with Session(engine) as session:
        yield session

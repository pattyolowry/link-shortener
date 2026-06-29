from datetime import datetime, timezone
from sqlmodel import Field, SQLModel

class Link(SQLModel, table=True):
    __tablename__ = "links"
    id: int | None = Field(default=None, primary_key=True)
    short_id: str = Field(unique=True)
    full_url: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )


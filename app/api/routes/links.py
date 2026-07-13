import os
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import text
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, AnyUrl
from typing import Annotated
from ...services.clients import short_id_generator
from ...services.db import get_session
from ...models import Link, LinkNoIndex

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

BASE_URL = os.getenv(
    "BASE_URL", "http://dum.my/"
)

class NewLinkResponse(BaseModel):
    fullUrl: AnyUrl
    shortUrl: AnyUrl

class Url(BaseModel):
    fullUrl: AnyUrl

@router.post("", response_model=NewLinkResponse, status_code=201)
async def create_short_url(url: Url, session: SessionDep):
    short_id = await short_id_generator.get_new_id()
    link = Link(
        short_id=short_id,
        full_url=str(url.fullUrl)
    )
    session.add(link)
    session.commit()
    session.refresh(link)

    return { "fullUrl": url.fullUrl, "shortUrl": f"{BASE_URL}/links/{short_id}"}

@router.get("/{short_id}", response_class=RedirectResponse, status_code=302)
def redirect_short_url(short_id: str, session: SessionDep):
    full_url = session.exec(
        text("SELECT full_url FROM links WHERE short_id = :short_id"),
        params={"short_id": short_id},
    ).first()
    if full_url is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url=full_url[0], status_code=302)
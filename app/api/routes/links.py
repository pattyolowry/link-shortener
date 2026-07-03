import os
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
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
    query = select(Link).where(Link.short_id == short_id)
    link = session.exec(query).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link.full_url
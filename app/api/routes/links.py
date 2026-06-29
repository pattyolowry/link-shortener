from fastapi import APIRouter, Depends
from sqlmodel import Session
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, AnyUrl
from typing import Annotated
from ...services.clients import short_id_generator
from ...services.db import get_session
from ...models import Link

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

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

    return { "fullUrl": url.fullUrl, "shortUrl": f"http://du.mmy/{short_id}"}

@router.get("/{short_id}", response_class=RedirectResponse, status_code=302)
async def redirect_short_url(short_id: str):
    return "https://www.wikipedia.org/"  
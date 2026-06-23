from fastapi import APIRouter
from pydantic import BaseModel, AnyUrl
from ...services.clients import short_id_generator

router = APIRouter()

class NewLinkResponse(BaseModel):
    fullUrl: AnyUrl
    shortUrl: AnyUrl

class Url(BaseModel):
    fullUrl: AnyUrl

@router.post("", response_model=NewLinkResponse, status_code=201)
async def create_short_url(url: Url):
    short_id = await short_id_generator.get_new_id()
    return { "fullUrl": url.fullUrl, "shortUrl": f"http://du.mmy/{short_id}"}
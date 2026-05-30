from fastapi import APIRouter
from pydantic import BaseModel, AnyUrl

router = APIRouter()

class NewLinkResponse(BaseModel):
    fullUrl: AnyUrl
    shortUrl: AnyUrl

class Url(BaseModel):
    fullUrl: AnyUrl

@router.post("/", response_model=NewLinkResponse, status_code=201)
def create_short_url(url: Url):
    return { "fullUrl": url.fullUrl, "shortUrl": "http://du.mmy/123456"}
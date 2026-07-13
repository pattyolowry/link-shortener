from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

router = APIRouter()

class PingResponse(BaseModel):
    message: str

@router.get("", response_model=PingResponse)
def send_ping() -> Any:
    return { "message": "Hello World!"}
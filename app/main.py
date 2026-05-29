from fastapi import FastAPI
from app.api.routes import ping

app = FastAPI(title="Link Shortener")

app.include_router(ping.router, prefix="/ping", tags=["ping"])